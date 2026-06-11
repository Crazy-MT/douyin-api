# 手动导出 secsdk 密钥（favorite 等接口需要）

## 快速导出（2 分钟）

在**已登录的抖音页面**（任意抖音网页，如 `https://www.douyin.com/?recommend=1`）：

### 1. 打开浏览器控制台
按 `F12` → 切到 `Console` 标签

### 2. 粘贴以下代码并回车
```javascript
(function(){
  var ls = {};
  for (var i=0;i<localStorage.length;i++){ 
    var k=localStorage.key(i); 
    ls[k]=localStorage.getItem(k); 
  }
  var out = JSON.stringify({
    localStorage: ls,
    cookie: document.cookie,
    href: location.href,
    ua: navigator.userAgent
  }, null, 2);
  
  // 创建下载
  var blob = new Blob([out], {type: 'application/json'});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'websign_env.json';
  a.click();
  
  console.log('✅ websign_env.json 已下载到你的下载文件夹');
  console.log('包含', Object.keys(ls).length, '个 localStorage 项');
  console.log('web_runtime_security_uid:', ls['web_runtime_security_uid']);
})()
```

### 3. 把下载的文件放到项目里
```
下载文件夹/websign_env.json  →  复制到  →  项目/lib/abogus_rebuild/websign_env.json
```

### 4. 同步导出当前页面的 cookie

再粘贴这段（导出与密钥同源的 cookie）：

```javascript
(function(){
  var jar = {};
  document.cookie.split('; ').forEach(function(c){
    var p = c.split('=');
    if(p[0]) jar[p[0]] = p[1] || '';
  });
  var out = JSON.stringify(jar);
  
  var blob = new Blob([out], {type: 'application/json'});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'cookie.json';
  a.click();
  
  console.log('✅ cookie.json 已下载');
  console.log('包含', Object.keys(jar).length, '个 cookie');
  console.log('sessionid:', jar.sessionid ? jar.sessionid.slice(0,12)+'...' : '无');
})()
```

把下载的 `cookie.json` 复制到 `项目/config/cookie.json`

### 5. 完成

重新运行代码，favorite 接口应该就能用了。密钥有效期数月，过期后重复上述步骤。

---

## 验证是否同源

导出后，在项目目录运行：
```bash
python -c "
import json
env = json.load(open('lib/abogus_rebuild/websign_env.json', encoding='utf-8'))
cfg = json.load(open('config/cookie.json', encoding='utf-8'))
env_uid = env['localStorage'].get('web_runtime_security_uid', '')
cfg_uid = cfg.get('x-web-secsdk-uid', '')
print('同源检查:', '✅ 一致' if env_uid == cfg_uid else '❌ 不一致')
print('  localStorage uid:', env_uid)
print('  cookie uid:', cfg_uid)
"
```

如果显示 `✅ 一致`，说明导出成功且同源。
