import 'package:douyin_flutter_debugger/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('debugger opens with user endpoints', (tester) async {
    await tester.pumpWidget(const DouyinDebuggerApp());

    expect(find.text('Douyin API Debugger'), findsOneWidget);
    expect(find.text('其他用户信息'), findsOneWidget);
    expect(find.text('发送请求'), findsOneWidget);

    await tester.tap(find.byTooltip('视频详情脚本'));
    await tester.pumpAndSettle();
    expect(find.text('aweme_id'), findsOneWidget);
    expect(find.text('获取并复制'), findsOneWidget);
  });
}
