import 'dart:io';

import 'package:flutter/material.dart';

import 'abogus_signer.dart';
import 'douyin_endpoint.dart';
import 'douyin_request.dart';
import 'mapping_builder.dart';

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
            tooltip: '生成映射表',
            onPressed: _showMappingDialog,
            icon: const Icon(Icons.table_chart),
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: Row(
        children: [
          SizedBox(
            width: 320,
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
                        leading: Icon(endpoint.method == EndpointMethod.post
                            ? Icons.upload
                            : Icons.download),
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

  Future<void> _showMappingDialog() async {
    final result = await showDialog<String>(
      context: context,
      builder: (_) => const MappingDialog(),
    );
    if (result == null || !mounted) return;
    try {
      await _signer.loadMappingFile(result);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('已加载映射表：${_signer.mappingCount} 样本')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('加载映射表失败：$error')),
      );
    }
  }
}

class MappingDialog extends StatefulWidget {
  const MappingDialog({super.key});

  @override
  State<MappingDialog> createState() => _MappingDialogState();
}

class _MappingDialogState extends State<MappingDialog> {
  late final _repoRoot = TextEditingController(text: _defaultRepoRoot());
  late final _outputPath = TextEditingController(
    text:
        '${_repoRoot.text}/douyin_flutter_debugger/assets/signing/time_mapping_sample.json',
  );
  final _start = TextEditingController(
    text: '${DateTime.now().millisecondsSinceEpoch}',
  );
  final _step = TextEditingController(text: '600000');
  final _count = TextEditingController(text: '10');
  final _logs = <String>[];
  var _running = false;

  @override
  void dispose() {
    _repoRoot.dispose();
    _outputPath.dispose();
    _start.dispose();
    _step.dispose();
    _count.dispose();
    super.dispose();
  }

  Future<void> _build() async {
    setState(() {
      _running = true;
      _logs
        ..clear()
        ..add('开始生成...');
    });
    try {
      final result = await MappingBuilder().build(
        repoRoot: _repoRoot.text.trim(),
        outputPath: _outputPath.text.trim(),
        startTimestamp: int.parse(_start.text.trim()),
        stepMillis: int.parse(_step.text.trim()),
        count: int.parse(_count.text.trim()),
      );
      setState(() {
        _logs
          ..clear()
          ..addAll(result.logs)
          ..add('新增: ${result.added}, 总样本: ${result.total}')
          ..add('已保存: ${result.outputPath}');
      });
    } catch (error) {
      setState(() => _logs.add('失败: $error'));
    } finally {
      if (mounted) setState(() => _running = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('生成 a_bogus 映射表'),
      content: SizedBox(
        width: 720,
        child: ListView(
          shrinkWrap: true,
          children: [
            const Text('调用仓库里的 Node bdms 补环境生成 a_bogus，再解码出 140 字节 bb。'),
            const SizedBox(height: 12),
            TextField(
                controller: _repoRoot,
                decoration: const InputDecoration(
                    labelText: '仓库根目录', border: OutlineInputBorder())),
            const SizedBox(height: 12),
            TextField(
                controller: _outputPath,
                decoration: const InputDecoration(
                    labelText: '输出 JSON', border: OutlineInputBorder())),
            const SizedBox(height: 12),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                SizedBox(
                    width: 220,
                    child: TextField(
                        controller: _start,
                        decoration: const InputDecoration(
                            labelText: '起始毫秒时间戳',
                            border: OutlineInputBorder()))),
                SizedBox(
                    width: 160,
                    child: TextField(
                        controller: _step,
                        decoration: const InputDecoration(
                            labelText: '步长 ms', border: OutlineInputBorder()))),
                SizedBox(
                    width: 120,
                    child: TextField(
                        controller: _count,
                        decoration: const InputDecoration(
                            labelText: '数量', border: OutlineInputBorder()))),
              ],
            ),
            const SizedBox(height: 12),
            DecoratedBox(
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceContainerHighest,
                borderRadius: BorderRadius.circular(6),
              ),
              child: SizedBox(
                height: 180,
                width: double.infinity,
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(12),
                  child:
                      SelectableText(_logs.isEmpty ? '尚未生成' : _logs.join('\n')),
                ),
              ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: _running ? null : () => Navigator.pop(context),
          child: const Text('关闭'),
        ),
        FilledButton.icon(
          onPressed: _running ? null : _build,
          icon: _running
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2))
              : const Icon(Icons.play_arrow),
          label: const Text('生成'),
        ),
        FilledButton.tonal(
          onPressed: _running
              ? null
              : () => Navigator.pop(context, _outputPath.text.trim()),
          child: const Text('加载此表'),
        ),
      ],
    );
  }

  String _defaultRepoRoot() {
    final cwd = Directory.current.path;
    if (File('$cwd/lib/runtime/bdms/index.js').existsSync()) return cwd;
    final parent = Directory(cwd).parent.path;
    if (File('$parent/lib/runtime/bdms/index.js').existsSync()) return parent;
    return '/Users/maotong/Desktop/project/douyin-api';
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
