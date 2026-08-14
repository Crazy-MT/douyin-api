import 'dart:convert';
import 'dart:io';

import 'package:path_provider/path_provider.dart';

import 'douyin_endpoint.dart';
import 'douyin_request.dart';

class AwemeDetailTool {
  const AwemeDetailTool(this._request);

  final DouyinRequest _request;

  Future<Map<String, dynamic>> fetchSummary({
    required String awemeId,
    required String cookie,
  }) async {
    final result = await _request.send(
      videoEndpoints.first,
      {'aweme_id': awemeId},
      cookie,
    );
    final data = jsonDecode(result.body) as Map<String, dynamic>;
    final detail = (data['aweme_detail'] as Map?) ?? const {};
    final author = (detail['author'] as Map?) ?? const {};
    final stats = (detail['statistics'] as Map?) ?? const {};
    final video = (detail['video'] as Map?) ?? const {};

    return {
      'http_status': result.statusCode,
      'status_code': data['status_code'],
      'aweme_id': detail['aweme_id'],
      'desc': detail['desc'],
      'author_nickname': author['nickname'],
      'author_uid': author['uid'],
      'create_time': _formatSeconds(detail['create_time']),
      'duration_ms': detail['duration'],
      'digg_count': stats['digg_count'],
      'comment_count': stats['comment_count'],
      'share_count': stats['share_count'],
      'collect_count': stats['collect_count'],
      'cover_url': _firstUrl((video['cover'] as Map?) ?? const {}),
      'play_url': _firstUrl((video['play_addr'] as Map?) ?? const {}),
    };
  }

  Future<String> downloadVideo({
    required Map<String, dynamic> summary,
    required String awemeId,
    required String cookie,
    required String outputPath,
  }) async {
    final playUrl = '${summary['play_url'] ?? ''}';
    if (playUrl.isEmpty) {
      throw StateError('没有可下载的 play_url');
    }
    final path = outputPath.trim().isEmpty
        ? await defaultDownloadPath(awemeId)
        : outputPath.trim();
    final file = File(path);
    try {
      if (file.parent.path != '.') {
        await file.parent.create(recursive: true);
      }
    } on FileSystemException catch (error) {
      throw FileSystemException(
        '无法创建下载目录；请保存到默认下载路径，或给 App 对应目录权限',
        error.path,
        error.osError,
      );
    }

    final client = HttpClient()
      ..connectionTimeout = const Duration(seconds: 20);
    final request = await client.getUrl(Uri.parse(playUrl));
    request.headers.set(
      HttpHeaders.userAgentHeader,
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    );
    request.headers.set(
        HttpHeaders.refererHeader, 'https://www.douyin.com/video/$awemeId');
    if (cookie.trim().isNotEmpty) {
      request.headers.set(HttpHeaders.cookieHeader, cookie.trim());
    }
    final response = await request.close();
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw HttpException('下载失败 HTTP ${response.statusCode}',
          uri: Uri.parse(playUrl));
    }
    try {
      await response.pipe(file.openWrite());
    } on FileSystemException catch (error) {
      throw FileSystemException(
        '无法写入视频文件；请保存到默认下载路径，或给 App 对应目录权限',
        error.path,
        error.osError,
      );
    }
    client.close(force: true);
    return file.path;
  }

  Future<String> defaultDownloadPath(String awemeId) async {
    Directory dir;
    if (Platform.isAndroid) {
      const androidDownloadDir = '/storage/emulated/0/Download';
      dir = Directory(androidDownloadDir);
      if (!await dir.exists()) {
        final externals = await getExternalStorageDirectories(
            type: StorageDirectory.downloads);
        if (externals != null && externals.isNotEmpty) {
          dir = externals.first;
        } else {
          dir = await getApplicationDocumentsDirectory();
        }
      }
    } else if (Platform.isIOS) {
      dir = await getApplicationDocumentsDirectory();
    } else {
      dir = await getDownloadsDirectory() ??
          await getApplicationDocumentsDirectory();
    }
    final subDir =
        Directory('${dir.path}${Platform.pathSeparator}douyin_video');
    return '${subDir.path}${Platform.pathSeparator}$awemeId.mp4';
  }

  String encodeSummary(Map<String, dynamic> summary) {
    return const JsonEncoder.withIndent('  ').convert(summary);
  }

  String? _firstUrl(Map obj) {
    final urls = obj['url_list'];
    if (urls is List && urls.isNotEmpty) return '${urls.first}';
    return null;
  }

  String? _formatSeconds(Object? value) {
    final seconds = value is int ? value : int.tryParse('$value');
    if (seconds == null) return null;
    final date = DateTime.fromMillisecondsSinceEpoch(seconds * 1000);
    String two(int n) => n.toString().padLeft(2, '0');
    return '${date.year}-${two(date.month)}-${two(date.day)} ${two(date.hour)}:${two(date.minute)}:${two(date.second)}';
  }
}
