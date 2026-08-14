import 'dart:convert';
import 'dart:io';

import 'package:douyin_flutter_debugger/mapping_builder.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('builds one mapping sample with bdms node runtime', () async {
    final output = File('/private/tmp/douyin_flutter_mapping_test.json');
    if (output.existsSync()) output.deleteSync();

    final result = await MappingBuilder().build(
      repoRoot: '/Users/maotong/Desktop/project/douyin-api',
      outputPath: output.path,
      startTimestamp: 1704067200000,
      stepMillis: 600000,
      count: 1,
    );

    final data =
        jsonDecode(await output.readAsString()) as Map<String, dynamic>;
    expect(result.added, 1);
    expect(data, contains('1704067200000'));
    expect(data['1704067200000'], hasLength(greaterThanOrEqualTo(140)));
  });
}
