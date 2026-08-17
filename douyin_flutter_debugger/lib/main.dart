import 'package:flutter/material.dart';

import 'abogus_signer.dart';
import 'aweme_detail_tool.dart';
import 'douyin_endpoint.dart';
import 'douyin_request.dart';

void main() => runApp(const DouyinDebuggerApp());

class DouyinDebuggerApp extends StatelessWidget {
  const DouyinDebuggerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Douyin API Debugger',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xff006d77)),
        useMaterial3: true,
        visualDensity: VisualDensity.compact,
      ),
      home: const DebuggerPage(),
    );
  }
}

class DebuggerPage extends StatefulWidget {
  const DebuggerPage({super.key});

  @override
  State<DebuggerPage> createState() => _DebuggerPageState();
}

class _DebuggerPageState extends State<DebuggerPage> {
  final _cookieController = TextEditingController();
  final _searchController = TextEditingController();
  final _signer = ABogusSigner();
  final _controllers = <String, TextEditingController>{};
  late final _request = DouyinRequest(_signer);
  EndpointGroup _group = EndpointGroup.user;
  DouyinEndpoint _endpoint = userEndpoints.first;
  DouyinResult? _result;
  String? _error;
  var _loading = false;

  Iterable<DouyinEndpoint> get _visibleEndpoints {
    final query = _searchController.text.trim().toLowerCase();
    return allEndpoints.where((endpoint) {
      if (endpoint.group != _group) return false;
      if (query.isEmpty) return true;
      return endpoint.title.toLowerCase().contains(query) ||
          endpoint.remoteUri.toLowerCase().contains(query);
    });
  }

  @override
  void initState() {
    super.initState();
    _syncControllers();
  }

  @override
  void dispose() {
    _cookieController.dispose();
    _searchController.dispose();
    for (final controller in _controllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  void _syncControllers() {
    final keys = {..._endpoint.params, ..._endpoint.defaults.keys};
    for (final key in keys) {
      _controllers.putIfAbsent(key,
          () => TextEditingController(text: _endpoint.defaults[key] ?? ''));
      if (_endpoint.defaults.containsKey(key) &&
          _controllers[key]!.text.isEmpty) {
        _controllers[key]!.text = _endpoint.defaults[key]!;
      }
    }
  }

  Future<void> _send() async {
    FocusScope.of(context).unfocus();
    setState(() {
      _loading = true;
      _error = null;
      _result = null;
    });
    try {
      final input = {
        for (final entry in _controllers.entries)
          if (entry.value.text.trim().isNotEmpty)
            entry.key: entry.value.text.trim(),
      };
      final result =
          await _request.send(_endpoint, input, _cookieController.text);
      setState(() => _result = result);
    } catch (error) {
      setState(() => _error = '$error');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _selectEndpoint(DouyinEndpoint endpoint) {
    setState(() {
      _endpoint = endpoint;
      _result = null;
      _error = null;
      _syncControllers();
    });
  }

  @override
  Widget build(BuildContext context) {
    final endpoints = _visibleEndpoints.toList();
    return Scaffold(
      appBar: AppBar(
        title: const Text('Douyin API Debugger'),
        actions: [
          SegmentedButton<EndpointGroup>(
            segments: const [
              ButtonSegment(
                  value: EndpointGroup.user,
                  icon: Icon(Icons.person_search),
                  label: Text('用户')),
              ButtonSegment(
                  value: EndpointGroup.video,
                  icon: Icon(Icons.smart_display),
                  label: Text('视频')),
            ],
            selected: {_group},
            onSelectionChanged: (value) {
              final group = value.first;
              setState(() {
                _group = group;
                _endpoint = group == EndpointGroup.user
                    ? userEndpoints.first
                    : videoEndpoints.first;
                _searchController.clear();
                _result = null;
                _error = null;
                _syncControllers();
              });
            },
          ),
          IconButton(
            tooltip: '视频详情脚本',
            onPressed: _showAwemeToolDialog,
            icon: const Icon(Icons.movie_filter),
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: Row(
        children: [
          SizedBox(
            width: 160,
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(12),
                  child: TextField(
                    controller: _searchController,
                    decoration: const InputDecoration(
                        prefixIcon: Icon(Icons.search),
                        hintText: '搜索接口',
                        border: OutlineInputBorder()),
                    onChanged: (_) => setState(() {}),
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: endpoints.length,
                    itemBuilder: (context, index) {
                      final endpoint = endpoints[index];
                      return ListTile(
                        selected: endpoint == _endpoint,
                        // leading: Icon(endpoint.method == EndpointMethod.post
                        //     ? Icons.upload
                        //     : Icons.download),
                        title: Text(endpoint.title,
                            maxLines: 1, overflow: TextOverflow.ellipsis),
                        subtitle: Text(endpoint.remoteUri,
                            maxLines: 1, overflow: TextOverflow.ellipsis),
                        onTap: () => _selectEndpoint(endpoint),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
          const VerticalDivider(width: 1),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Text(_endpoint.title,
                    style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 6),
                SelectableText(
                    '${_endpoint.method.name.toUpperCase()} ${_endpoint.remoteUri}'),
                if (_endpoint.needsWebSign)
                  const Padding(
                    padding: EdgeInsets.only(top: 8),
                    child: Text(
                        '此接口 Python 版还会补 secsdk web-signature；Dart 端先用于调参和验证 a_bogus。'),
                  ),
                const SizedBox(height: 16),
                TextField(
                  controller: _cookieController,
                  minLines: 2,
                  maxLines: 5,
                  decoration: const InputDecoration(
                    labelText: 'Cookie',
                    hintText: '支持浏览器 cookie 字符串或 JSON cookie',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    for (final key in {
                      ..._endpoint.params,
                      ..._endpoint.defaults.keys
                    })
                      SizedBox(
                        width: 280,
                        child: TextField(
                          controller: _controllers[key],
                          decoration: InputDecoration(
                            labelText: key,
                            border: const OutlineInputBorder(),
                            suffixIcon: _endpoint.defaults.containsKey(key)
                                ? const Tooltip(
                                    message: '默认参数', child: Icon(Icons.tune))
                                : null,
                          ),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 16),
                Align(
                  alignment: Alignment.centerLeft,
                  child: FilledButton.icon(
                    onPressed: _loading ? null : _send,
                    icon: _loading
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(strokeWidth: 2))
                        : const Icon(Icons.play_arrow),
                    label: const Text('发送请求'),
                  ),
                ),
                const SizedBox(height: 16),
                if (_error != null)
                  SelectableText(_error!,
                      style: TextStyle(
                          color: Theme.of(context).colorScheme.error)),
                if (_result != null) _ResultView(result: _result!),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _showAwemeToolDialog() async {
    await showDialog<void>(
      context: context,
      builder: (_) => AwemeDetailDialog(
        tool: AwemeDetailTool(_request),
        cookie: _cookieController.text,
      ),
    );
  }
}

class AwemeDetailDialog extends StatefulWidget {
  const AwemeDetailDialog({
    super.key,
    required this.tool,
    required this.cookie,
  });

  final AwemeDetailTool tool;
  final String cookie;

  @override
  State<AwemeDetailDialog> createState() => _AwemeDetailDialogState();
}

class _AwemeDetailDialogState extends State<AwemeDetailDialog> {
  final _awemeId = TextEditingController();
  final _outputPath = TextEditingController();
  Map<String, dynamic>? _summary;
  String? _message;
  var _loading = false;
  var _downloading = false;

  @override
  void initState() {
    super.initState();
    _refreshDefaultOutputPath(force: true);
    _awemeId.addListener(_syncDefaultOutputPath);
  }

  @override
  void dispose() {
    _awemeId.removeListener(_syncDefaultOutputPath);
    _awemeId.dispose();
    _outputPath.dispose();
    super.dispose();
  }

  void _syncDefaultOutputPath() {
    final awemeId = _awemeId.text.trim();
    if (awemeId.isEmpty) return;
    final current = _outputPath.text.trim();
    if (current.isEmpty || RegExp(r'[/\\][^/\\]+\.mp4$').hasMatch(current)) {
      _refreshDefaultOutputPath();
    }
  }

  Future<void> _refreshDefaultOutputPath({bool force = false}) async {
    final awemeId = _awemeId.text.trim();
    if (awemeId.isEmpty) return;
    final current = _outputPath.text.trim();
    if (!force &&
        current.isNotEmpty &&
        !RegExp(r'[/\\][^/\\]+\.mp4$').hasMatch(current)) {
      return;
    }
    final path = await widget.tool.defaultDownloadPath(awemeId);
    if (mounted) _outputPath.text = path;
  }

  Future<void> _fetch() async {
    final awemeId = _awemeId.text.trim();
    if (awemeId.isEmpty) {
      setState(() => _message = '请输入 aweme_id');
      return;
    }
    setState(() {
      _loading = true;
      _message = null;
      _summary = null;
    });
    try {
      final summary = await widget.tool.fetchSummary(
        awemeId: awemeId,
        cookie: widget.cookie,
      );
      /*await Clipboard.setData(
        ClipboardData(text: widget.tool.encodeSummary(summary)),
      );*/
      setState(() {
        _summary = summary;
        _message = '已复制到剪贴板';
      });
    } catch (error) {
      setState(() => _message = '获取失败：$error');
      debugPrint(_summary.toString());
      debugPrint(error.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _download() async {
    final summary = _summary;
    if (summary == null) {
      setState(() => _message = '请先获取视频详情');
      return;
    }
    setState(() {
      _downloading = true;
      _message = null;
    });
    try {
      final path = await widget.tool.downloadVideo(
        summary: summary,
        awemeId: _awemeId.text.trim(),
        cookie: widget.cookie,
        outputPath: _outputPath.text,
      );
      setState(() => _message = '已下载: $path');
    } catch (error) {
      setState(() => _message = '下载失败：$error');
    } finally {
      if (mounted) setState(() => _downloading = false);
    }
    debugPrint(_message);
  }

  @override
  Widget build(BuildContext context) {
    final summaryText =
        _summary == null ? '尚未获取' : widget.tool.encodeSummary(_summary!);
    return AlertDialog(
      title: const Text('视频详情脚本'),
      content: SizedBox(
        width: 720,
        child: ListView(
          shrinkWrap: true,
          children: [
            TextField(
              controller: _awemeId,
              decoration: const InputDecoration(
                labelText: 'aweme_id',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _outputPath,
              decoration: const InputDecoration(
                labelText: '下载路径',
                hintText: '建议保存到 Downloads',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            if (_message != null) Text(_message!),
            const SizedBox(height: 12),
            DecoratedBox(
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceContainerHighest,
                borderRadius: BorderRadius.circular(6),
              ),
              child: SizedBox(
                width: double.infinity,
                height: 260,
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(12),
                  child: SelectableText(summaryText),
                ),
              ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed:
              (_loading || _downloading) ? null : () => Navigator.pop(context),
          child: const Text('关闭'),
        ),
        FilledButton.icon(
          onPressed: _loading ? null : _fetch,
          icon: _loading
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.content_copy),
          label: const Text('获取并复制'),
        ),
        FilledButton.tonalIcon(
          onPressed: _downloading ? null : _download,
          icon: _downloading
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.download),
          label: const Text('下载视频'),
        ),
      ],
    );
  }
}

class _ResultView extends StatelessWidget {
  const _ResultView({required this.result});

  final DouyinResult result;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('HTTP ${result.statusCode} · ${result.elapsed.inMilliseconds} ms',
            style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        SelectableText(result.url),
        if (result.warning != null)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Text(result.warning!,
                style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ),
        const SizedBox(height: 12),
        DecoratedBox(
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceContainerHighest,
            borderRadius: BorderRadius.circular(6),
          ),
          child: SizedBox(
            width: double.infinity,
            child: Padding(
              padding: const EdgeInsets.all(12),
              child:
                  SelectableText(result.body.isEmpty ? '<empty>' : result.body),
            ),
          ),
        ),
      ],
    );
  }
}
