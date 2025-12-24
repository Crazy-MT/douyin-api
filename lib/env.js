/**
 * bdms.js 运行环境模拟
 * 用于在 Node.js 中运行 bdms.js
 */

// 隐藏 Node.js 环境特征，让 bdms.js 认为在浏览器中运行
// bdms.js 564行检测: "undefined" != typeof process && "process" == n(process)
global._process = global.process;
delete global.process;

// 最先定义全局函数，避免 bdms 加载时找不到
global.requestAnimationFrame = function(cb) { return setTimeout(cb, 16); };
global.cancelAnimationFrame = function(id) { clearTimeout(id); };

// 破坏 URLSearchParams 检测，让 bdms 重写 fetch
// 模块 5406 检测：!r.size && (u || !i)
// 让 size 属性不存在，检测就会失败
Object.defineProperty(URLSearchParams.prototype, 'size', {
    get: function() {
        throw new Error('size not supported');
    },
    configurable: true
});

// 全局变量存储 a_bogus
var windows = {
    a_bogus: null
};

// 模拟 window 对象
var window = {
    bdms: null,
    __ac_referer: "",
    location: {
        href: "https://www.douyin.com/",
        pathname: "/",
        search: "",
        host: "www.douyin.com",
        hostname: "www.douyin.com",
        protocol: "https:",
        origin: "https://www.douyin.com"
    },
    navigator: {
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        platform: "Win32",
        language: "zh-CN",
        languages: ["zh-CN", "zh"],
        cookieEnabled: true,
        onLine: true,
        hardwareConcurrency: 16,
        deviceMemory: 8,
        maxTouchPoints: 0,
        appName: "Netscape",
        appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        vendor: "Google Inc.",
        vendorSub: "",
        productSub: "20030107",
        product: "Gecko",
        appCodeName: "Mozilla",
        doNotTrack: null,
        plugins: { length: 0 },
        mimeTypes: { length: 0 },
        webdriver: false,
        getBattery: function() {
            return Promise.resolve({
                charging: true,
                chargingTime: 0,
                dischargingTime: Infinity,
                level: 1
            });
        },
        sendBeacon: function() { return true; },
        getGamepads: function() { return []; },
        javaEnabled: function() { return false; },
        vibrate: function() { return false; },
        requestMediaKeySystemAccess: function() { return Promise.reject(); },
        mediaDevices: {
            enumerateDevices: function() { return Promise.resolve([]); },
            getUserMedia: function() { return Promise.reject(); }
        },
        permissions: {
            query: function() { return Promise.resolve({ state: 'prompt' }); }
        },
        connection: {
            effectiveType: '4g',
            downlink: 10,
            rtt: 50,
            saveData: false
        },
        storage: {
            estimate: function() { return Promise.resolve({ quota: 0, usage: 0 }); }
        },
        clipboard: {
            writeText: function() { return Promise.resolve(); },
            readText: function() { return Promise.resolve(''); }
        },
        credentials: {
            get: function() { return Promise.resolve(null); },
            create: function() { return Promise.resolve(null); }
        },
        serviceWorker: null,
        geolocation: null
    },
    screen: {
        width: 1920,
        height: 1080,
        availWidth: 1920,
        availHeight: 1040,
        colorDepth: 24,
        pixelDepth: 24
    },
    devicePixelRatio: 1,
    innerWidth: 1920,
    innerHeight: 900,
    outerWidth: 1920,
    outerHeight: 1040,
    screenX: 0,
    screenY: 0,
    pageXOffset: 0,
    pageYOffset: 0,
    scrollX: 0,
    scrollY: 0,
    localStorage: {
        getItem: function(key) { return null; },
        setItem: function(key, value) {},
        removeItem: function(key) {},
        clear: function() {}
    },
    sessionStorage: {
        getItem: function(key) { return null; },
        setItem: function(key, value) {},
        removeItem: function(key) {},
        clear: function() {}
    },
    origin: "https://www.douyin.com",
    isSecureContext: true,
    indexedDB: {},
    caches: {},
    cookieStore: {},
    performance: {
        now: function() { return Date.now(); },
        timing: {
            navigationStart: Date.now() - 1000
        }
    },
    history: {
        length: 1
    },
    crypto: {
        getRandomValues: function(arr) {
            for (var i = 0; i < arr.length; i++) {
                arr[i] = Math.floor(Math.random() * 256);
            }
            return arr;
        }
    },
    _eventListeners: {},
    addEventListener: function(type, listener, options) {
        if (!this._eventListeners[type]) {
            this._eventListeners[type] = [];
        }
        this._eventListeners[type].push(listener);
    },
    removeEventListener: function(type, listener) {
        if (this._eventListeners[type]) {
            var idx = this._eventListeners[type].indexOf(listener);
            if (idx > -1) {
                this._eventListeners[type].splice(idx, 1);
            }
        }
    },
    dispatchEvent: function(event) {
        var type = event.type;
        if (this._eventListeners[type]) {
            for (var i = 0; i < this._eventListeners[type].length; i++) {
                try {
                    this._eventListeners[type][i].call(this, event);
                } catch(e) {}
            }
        }
        return true;
    },
    setTimeout: setTimeout,
    setInterval: setInterval,
    clearTimeout: clearTimeout,
    clearInterval: clearInterval,
    requestAnimationFrame: function(cb) { return setTimeout(cb, 16); },
    cancelAnimationFrame: function(id) { clearTimeout(id); },
    atob: function(str) {
        return Buffer.from(str, 'base64').toString('binary');
    },
    btoa: function(str) {
        return Buffer.from(str, 'binary').toString('base64');
    },
    fetch: function(url, options) {
        // 模拟 fetch Response
        return Promise.resolve({
            ok: true,
            status: 200,
            statusText: 'OK',
            url: typeof url === 'string' ? url : url.url,
            headers: new Map(),
            json: function() { return Promise.resolve({}); },
            text: function() { return Promise.resolve(''); },
            blob: function() { return Promise.resolve(new Blob()); },
            arrayBuffer: function() { return Promise.resolve(new ArrayBuffer(0)); },
            clone: function() { return this; }
        });
    }
};

// 模拟 XMLHttpRequest 类
function XMLHttpRequest() {
    this.readyState = 0;
    this.status = 0;
    this.statusText = '';
    this.responseText = '';
    this.responseType = '';
    this.response = null;
    this.timeout = 0;
    this.withCredentials = false;
    this._url = '';
    this._method = 'GET';
    this._headers = {};
    this._listeners = {};
}

XMLHttpRequest.prototype.open = function(method, url, async) {
    this._method = method;
    this._url = url;
    this.readyState = 1;
};

XMLHttpRequest.prototype.setRequestHeader = function(name, value) {
    this._headers[name] = value;
};

XMLHttpRequest.prototype.send = function(data) {
    var self = this;
    this.readyState = 4;
    this.status = 200;
    this.statusText = 'OK';
    this.responseText = '{}';
    this.response = {};

    // 触发 readystatechange 事件
    if (typeof this.onreadystatechange === 'function') {
        this.onreadystatechange();
    }

    // 触发 load 事件
    if (typeof this.onload === 'function') {
        this.onload();
    }

    // 触发事件监听器
    this._triggerEvent('readystatechange');
    this._triggerEvent('load');
};

XMLHttpRequest.prototype.abort = function() {
    this.readyState = 0;
};

XMLHttpRequest.prototype.addEventListener = function(type, listener) {
    if (!this._listeners[type]) {
        this._listeners[type] = [];
    }
    this._listeners[type].push(listener);
};

XMLHttpRequest.prototype.removeEventListener = function(type, listener) {
    if (this._listeners[type]) {
        var idx = this._listeners[type].indexOf(listener);
        if (idx > -1) {
            this._listeners[type].splice(idx, 1);
        }
    }
};

XMLHttpRequest.prototype._triggerEvent = function(type) {
    if (!this._listeners) {
        this._listeners = {};
    }
    var listeners = this._listeners[type];
    if (listeners) {
        var event = { type: type, target: this };
        for (var i = 0; i < listeners.length; i++) {
            listeners[i].call(this, event);
        }
    }
};

XMLHttpRequest.prototype.getResponseHeader = function(name) {
    return null;
};

XMLHttpRequest.prototype.getAllResponseHeaders = function() {
    return '';
};

// window 上挂载 XMLHttpRequest
window.XMLHttpRequest = XMLHttpRequest;

// 模拟 document 对象
var document = {
    domain: "www.douyin.com",
    referrer: "",
    cookie: "",
    title: "抖音",
    URL: "https://www.douyin.com/",
    visibilityState: "visible",
    hidden: false,
    hasFocus: function() { return true; },
    activeElement: null,
    documentElement: {
        clientWidth: 1920,
        clientHeight: 900
    },
    head: {},
    body: {
        clientWidth: 1920,
        clientHeight: 900
    },
    all: [],
    createElement: function(tag) {
        tag = tag.toLowerCase();
        if (tag === 'canvas') {
            return new HTMLCanvasElement();
        }
        return {
            tagName: tag.toUpperCase(),
            style: {},
            setAttribute: function() {},
            getAttribute: function() { return null; },
            appendChild: function() {},
            removeChild: function() {},
            addEventListener: function() {},
            removeEventListener: function() {},
            getContext: function() { return null; }
        };
    },
    getElementById: function() { return null; },
    getElementsByTagName: function() { return []; },
    getElementsByClassName: function() { return []; },
    querySelector: function() { return null; },
    querySelectorAll: function() { return []; },
    _eventListeners: {},
    addEventListener: function(type, listener, options) {
        if (!this._eventListeners[type]) {
            this._eventListeners[type] = [];
        }
        this._eventListeners[type].push(listener);
    },
    removeEventListener: function(type, listener) {
        if (this._eventListeners[type]) {
            var idx = this._eventListeners[type].indexOf(listener);
            if (idx > -1) {
                this._eventListeners[type].splice(idx, 1);
            }
        }
    },
    dispatchEvent: function(event) {
        var type = event.type;
        if (this._eventListeners[type]) {
            for (var i = 0; i < this._eventListeners[type].length; i++) {
                try {
                    this._eventListeners[type][i].call(this, event);
                } catch(e) {}
            }
        }
        return true;
    },
    createEvent: function() {
        return {
            initEvent: function() {}
        };
    }
};

// 模拟 navigator
var navigator = window.navigator;

// 模拟 location
var location = window.location;

// 模拟 screen
var screen = window.screen;

// 模拟 XMLHttpRequest
function XMLHttpRequest() {
    this.readyState = 0;
    this.status = 0;
    this.statusText = '';
    this.responseText = '';
    this.response = '';
    this.responseType = '';
    this.timeout = 0;
    this.withCredentials = false;
    this._headers = {};
}
XMLHttpRequest.prototype.open = function(method, url, async) {
    this._method = method;
    this._url = url;
    this._async = async !== false;
    this.readyState = 1;
};
XMLHttpRequest.prototype.setRequestHeader = function(name, value) {
    this._headers[name] = value;
};
XMLHttpRequest.prototype.send = function(data) {
    this.readyState = 4;
    this.status = 200;
    // 不真正发送请求，只是模拟
};
XMLHttpRequest.prototype.abort = function() {};
XMLHttpRequest.prototype.getAllResponseHeaders = function() { return ''; };
XMLHttpRequest.prototype.getResponseHeader = function(name) { return null; };
XMLHttpRequest.prototype.addEventListener = function() {};
XMLHttpRequest.prototype.removeEventListener = function() {};
XMLHttpRequest.UNSENT = 0;
XMLHttpRequest.OPENED = 1;
XMLHttpRequest.HEADERS_RECEIVED = 2;
XMLHttpRequest.LOADING = 3;
XMLHttpRequest.DONE = 4;

// 模拟 Image
function Image(width, height) {
    this.width = width || 0;
    this.height = height || 0;
    this.src = '';
    this.onload = null;
    this.onerror = null;
    this.complete = false;
    this.naturalWidth = 0;
    this.naturalHeight = 0;
}

// 模拟 Audio
function Audio(src) {
    this.src = src || '';
    this.volume = 1;
    this.muted = false;
    this.paused = true;
    this.play = function() { return Promise.resolve(); };
    this.pause = function() {};
    this.load = function() {};
}

// 模拟 MutationObserver
function MutationObserver(callback) {
    this._callback = callback;
}
MutationObserver.prototype.observe = function(target, options) {};
MutationObserver.prototype.disconnect = function() {};
MutationObserver.prototype.takeRecords = function() { return []; };

// 模拟 ResizeObserver
function ResizeObserver(callback) {
    this._callback = callback;
}
ResizeObserver.prototype.observe = function(target) {};
ResizeObserver.prototype.unobserve = function(target) {};
ResizeObserver.prototype.disconnect = function() {};

// 模拟 IntersectionObserver
function IntersectionObserver(callback, options) {
    this._callback = callback;
    this._options = options;
}
IntersectionObserver.prototype.observe = function(target) {};
IntersectionObserver.prototype.unobserve = function(target) {};
IntersectionObserver.prototype.disconnect = function() {};

// 模拟 PerformanceObserver
function PerformanceObserver(callback) {
    this._callback = callback;
}
PerformanceObserver.prototype.observe = function(options) {};
PerformanceObserver.prototype.disconnect = function() {};

// 模拟 WebSocket
function WebSocket(url, protocols) {
    this.url = url;
    this.readyState = 0;
    this.onopen = null;
    this.onclose = null;
    this.onerror = null;
    this.onmessage = null;
}
WebSocket.prototype.send = function(data) {};
WebSocket.prototype.close = function() { this.readyState = 3; };
WebSocket.CONNECTING = 0;
WebSocket.OPEN = 1;
WebSocket.CLOSING = 2;
WebSocket.CLOSED = 3;

// 模拟 Worker
function Worker(url) {
    this.onmessage = null;
    this.onerror = null;
}
Worker.prototype.postMessage = function(data) {};
Worker.prototype.terminate = function() {};

// 模拟 Blob
function Blob(parts, options) {
    this.size = 0;
    this.type = options && options.type || '';
    if (parts) {
        for (var i = 0; i < parts.length; i++) {
            if (typeof parts[i] === 'string') {
                this.size += parts[i].length;
            } else if (parts[i] instanceof ArrayBuffer) {
                this.size += parts[i].byteLength;
            }
        }
    }
}
Blob.prototype.slice = function(start, end, type) { return new Blob(); };
Blob.prototype.text = function() { return Promise.resolve(''); };
Blob.prototype.arrayBuffer = function() { return Promise.resolve(new ArrayBuffer(0)); };

// 模拟 File
function File(parts, name, options) {
    Blob.call(this, parts, options);
    this.name = name;
    this.lastModified = Date.now();
}
File.prototype = Object.create(Blob.prototype);

// 模拟 FileReader
function FileReader() {
    this.result = null;
    this.readyState = 0;
    this.onload = null;
    this.onerror = null;
}
FileReader.prototype.readAsText = function(blob) {};
FileReader.prototype.readAsDataURL = function(blob) {};
FileReader.prototype.readAsArrayBuffer = function(blob) {};

// 模拟 Canvas 相关对象
function CanvasRenderingContext2D() {
    this.canvas = null;
    this.fillStyle = '#000000';
    this.strokeStyle = '#000000';
    this.lineWidth = 1;
    this.font = '10px sans-serif';
    this.textAlign = 'start';
    this.textBaseline = 'alphabetic';
    this.globalAlpha = 1;
    this.globalCompositeOperation = 'source-over';
}
CanvasRenderingContext2D.prototype.fillRect = function() {};
CanvasRenderingContext2D.prototype.strokeRect = function() {};
CanvasRenderingContext2D.prototype.clearRect = function() {};
CanvasRenderingContext2D.prototype.fillText = function() {};
CanvasRenderingContext2D.prototype.strokeText = function() {};
CanvasRenderingContext2D.prototype.measureText = function(text) {
    return { width: text.length * 10 };
};
CanvasRenderingContext2D.prototype.beginPath = function() {};
CanvasRenderingContext2D.prototype.closePath = function() {};
CanvasRenderingContext2D.prototype.moveTo = function() {};
CanvasRenderingContext2D.prototype.lineTo = function() {};
CanvasRenderingContext2D.prototype.arc = function() {};
CanvasRenderingContext2D.prototype.arcTo = function() {};
CanvasRenderingContext2D.prototype.rect = function() {};
CanvasRenderingContext2D.prototype.fill = function() {};
CanvasRenderingContext2D.prototype.stroke = function() {};
CanvasRenderingContext2D.prototype.clip = function() {};
CanvasRenderingContext2D.prototype.save = function() {};
CanvasRenderingContext2D.prototype.restore = function() {};
CanvasRenderingContext2D.prototype.translate = function() {};
CanvasRenderingContext2D.prototype.rotate = function() {};
CanvasRenderingContext2D.prototype.scale = function() {};
CanvasRenderingContext2D.prototype.transform = function() {};
CanvasRenderingContext2D.prototype.setTransform = function() {};
CanvasRenderingContext2D.prototype.drawImage = function() {};
CanvasRenderingContext2D.prototype.createLinearGradient = function() {
    return { addColorStop: function() {} };
};
CanvasRenderingContext2D.prototype.createRadialGradient = function() {
    return { addColorStop: function() {} };
};
CanvasRenderingContext2D.prototype.createPattern = function() { return null; };
CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {
    return { data: new Uint8ClampedArray(w * h * 4), width: w, height: h };
};
CanvasRenderingContext2D.prototype.putImageData = function() {};
CanvasRenderingContext2D.prototype.createImageData = function(w, h) {
    return { data: new Uint8ClampedArray(w * h * 4), width: w, height: h };
};

function WebGLRenderingContext() {
    this.canvas = null;
    this.drawingBufferWidth = 300;
    this.drawingBufferHeight = 150;
}
WebGLRenderingContext.prototype.getParameter = function(pname) {
    var params = {
        37445: 'Intel Inc.',  // UNMASKED_VENDOR_WEBGL
        37446: 'Intel Iris OpenGL Engine',  // UNMASKED_RENDERER_WEBGL
        7936: 'WebKit',  // VENDOR
        7937: 'WebKit WebGL',  // RENDERER
        7938: 'WebGL 1.0',  // VERSION
        7939: 'WebGL GLSL ES 1.0',  // SHADING_LANGUAGE_VERSION
        3379: 16384,  // MAX_TEXTURE_SIZE
        34076: 16384,  // MAX_CUBE_MAP_TEXTURE_SIZE
        34024: 16384,  // MAX_RENDERBUFFER_SIZE
        35661: 80,  // MAX_COMBINED_TEXTURE_IMAGE_UNITS
        34930: 16,  // MAX_TEXTURE_IMAGE_UNITS
        35660: 16,  // MAX_VERTEX_TEXTURE_IMAGE_UNITS
        36347: 1024,  // MAX_VERTEX_UNIFORM_VECTORS
        36348: 1024,  // MAX_FRAGMENT_UNIFORM_VECTORS
        36349: 32,  // MAX_VARYING_VECTORS
        34921: 16,  // MAX_VERTEX_ATTRIBS
    };
    return params[pname] !== undefined ? params[pname] : null;
};
WebGLRenderingContext.prototype.getExtension = function(name) {
    if (name === 'WEBGL_debug_renderer_info') {
        return { UNMASKED_VENDOR_WEBGL: 37445, UNMASKED_RENDERER_WEBGL: 37446 };
    }
    return null;
};
WebGLRenderingContext.prototype.getSupportedExtensions = function() {
    return ['WEBGL_debug_renderer_info', 'OES_texture_float'];
};
WebGLRenderingContext.prototype.createShader = function() { return {}; };
WebGLRenderingContext.prototype.shaderSource = function() {};
WebGLRenderingContext.prototype.compileShader = function() {};
WebGLRenderingContext.prototype.getShaderParameter = function() { return true; };
WebGLRenderingContext.prototype.createProgram = function() { return {}; };
WebGLRenderingContext.prototype.attachShader = function() {};
WebGLRenderingContext.prototype.linkProgram = function() {};
WebGLRenderingContext.prototype.getProgramParameter = function() { return true; };
WebGLRenderingContext.prototype.useProgram = function() {};
WebGLRenderingContext.prototype.getShaderInfoLog = function() { return ''; };
WebGLRenderingContext.prototype.getProgramInfoLog = function() { return ''; };
WebGLRenderingContext.prototype.deleteShader = function() {};
WebGLRenderingContext.prototype.deleteProgram = function() {};
WebGLRenderingContext.prototype.getContextAttributes = function() {
    return { alpha: true, antialias: true, depth: true, stencil: false };
};

function HTMLCanvasElement() {
    this.width = 300;
    this.height = 150;
    this._context2d = new CanvasRenderingContext2D();
    this._context2d.canvas = this;
}
HTMLCanvasElement.prototype.getContext = function(type) {
    if (type === '2d') {
        return this._context2d;
    } else if (type === 'webgl' || type === 'experimental-webgl') {
        return new WebGLRenderingContext();
    }
    return null;
};
HTMLCanvasElement.prototype.toDataURL = function(type) {
    // 返回一个固定的 base64 字符串
    return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
};
HTMLCanvasElement.prototype.toBlob = function(callback, type, quality) {
    callback(new Blob([''], { type: type || 'image/png' }));
};

// 模拟 URL
var _URL = {
    createObjectURL: function(blob) { return 'blob:' + Math.random().toString(36); },
    revokeObjectURL: function(url) {}
};

// 模拟 self 和 globalThis
var self = window;
if (typeof globalThis === 'undefined') {
    var globalThis = global;
}
globalThis.window = window;
globalThis.document = document;
globalThis.navigator = navigator;
globalThis.location = location;
globalThis.screen = screen;
globalThis.self = self;
globalThis.windows = windows;
globalThis.XMLHttpRequest = XMLHttpRequest;
globalThis.Image = Image;
globalThis.Audio = Audio;
globalThis.MutationObserver = MutationObserver;
globalThis.WebKitMutationObserver = MutationObserver;
globalThis.ResizeObserver = ResizeObserver;
globalThis.IntersectionObserver = IntersectionObserver;
globalThis.PerformanceObserver = PerformanceObserver;
globalThis.WebSocket = WebSocket;
globalThis.Worker = Worker;
globalThis.Blob = Blob;
globalThis.File = File;
globalThis.FileReader = FileReader;
globalThis.CanvasRenderingContext2D = CanvasRenderingContext2D;
globalThis.WebGLRenderingContext = WebGLRenderingContext;
globalThis.HTMLCanvasElement = HTMLCanvasElement;
globalThis.requestAnimationFrame = window.requestAnimationFrame;
globalThis.cancelAnimationFrame = window.cancelAnimationFrame;

// 重写全局 fetch，让 bdms.js 能够拦截它
globalThis.fetch = window.fetch;
globalThis.URL = globalThis.URL || _URL;

// 模拟 Headers 类（让 bdms 可以重写 fetch）
function Headers(init) {
    this._headers = {};
    if (init) {
        if (init instanceof Headers) {
            this._headers = Object.assign({}, init._headers);
        } else if (typeof init === 'object') {
            for (var key in init) {
                if (init.hasOwnProperty(key)) {
                    this._headers[key.toLowerCase()] = init[key];
                }
            }
        }
    }
}
Headers.prototype.append = function(name, value) {
    this._headers[name.toLowerCase()] = value;
};
Headers.prototype.delete = function(name) {
    delete this._headers[name.toLowerCase()];
};
Headers.prototype.get = function(name) {
    return this._headers[name.toLowerCase()] || null;
};
Headers.prototype.has = function(name) {
    return name.toLowerCase() in this._headers;
};
Headers.prototype.set = function(name, value) {
    this._headers[name.toLowerCase()] = value;
};
Headers.prototype.forEach = function(callback) {
    for (var key in this._headers) {
        callback(this._headers[key], key, this);
    }
};
globalThis.Headers = Headers;

// 模拟 Request 类
function Request(input, init) {
    this.url = typeof input === 'string' ? input : input.url;
    this.method = (init && init.method) || 'GET';
    this.headers = new Headers((init && init.headers) || {});
    this.body = (init && init.body) || null;
}
globalThis.Request = Request;

globalThis.atob = function(str) {
    return Buffer.from(str, 'base64').toString('binary');
};
globalThis.btoa = function(str) {
    return Buffer.from(str, 'binary').toString('base64');
};

// 模拟 queueMicrotask
if (typeof queueMicrotask === 'undefined') {
    var queueMicrotask = function(callback) {
        Promise.resolve().then(callback);
    };
}

// 模拟 TextDecoder 和 TextEncoder
if (typeof TextDecoder === 'undefined') {
    var TextDecoder = require('util').TextDecoder;
}
if (typeof TextEncoder === 'undefined') {
    var TextEncoder = require('util').TextEncoder;
}

// 钩住 URLSearchParams.prototype.set 来捕获 a_bogus
const originalURLSearchParamsSet = URLSearchParams.prototype.set;
URLSearchParams.prototype.set = function(key, value) {
    if (key === 'a_bogus') {
        windows.a_bogus = value;
        // console.log('[Hook] a_bogus captured:', value);
    }
    return originalURLSearchParamsSet.call(this, key, value);
};

// 导出环境变量
module.exports = {
    window: window,
    document: document,
    navigator: navigator,
    location: location,
    screen: screen,
    self: self,
    globalThis: globalThis,
    windows: windows,

    // 更新环境配置的方法
    updateLocation: function(url) {
        try {
            var urlObj = new URL(url);
            window.location.href = url;
            window.location.pathname = urlObj.pathname;
            window.location.search = urlObj.search;
            window.location.host = urlObj.host;
            window.location.hostname = urlObj.hostname;
            window.location.protocol = urlObj.protocol;
            window.location.origin = urlObj.origin;
            document.URL = url;
        } catch (e) {
            console.error("Invalid URL:", url);
        }
    },

    updateUserAgent: function(ua) {
        window.navigator.userAgent = ua;
        navigator.userAgent = ua;
    },

    updateScreen: function(width, height) {
        window.screen.width = width;
        window.screen.height = height;
        screen.width = width;
        screen.height = height;
    },

    // 获取 a_bogus 值
    getABogus: function() {
        return windows.a_bogus;
    },

    // 重置 a_bogus 值
    resetABogus: function() {
        windows.a_bogus = null;
    },

    // 触发鼠标移动事件（bdms 需要至少一次鼠标事件才能生成有效签名）
    triggerMouseEvent: function() {
        var mouseEvent = {
            type: 'mousemove',
            clientX: Math.floor(Math.random() * 1000),
            clientY: Math.floor(Math.random() * 800),
            screenX: Math.floor(Math.random() * 1000),
            screenY: Math.floor(Math.random() * 800),
            pageX: Math.floor(Math.random() * 1000),
            pageY: Math.floor(Math.random() * 800),
            movementX: Math.floor(Math.random() * 10),
            movementY: Math.floor(Math.random() * 10),
            target: document.body || document,
            currentTarget: document,
            bubbles: true,
            cancelable: true,
            timeStamp: Date.now(),
            isTrusted: true
        };
        // 触发 window 上的事件
        if (window._eventListeners && window._eventListeners['mousemove']) {
            for (var i = 0; i < window._eventListeners['mousemove'].length; i++) {
                try {
                    window._eventListeners['mousemove'][i].call(window, mouseEvent);
                } catch(e) {}
            }
        }
        // 触发 document 上的事件
        if (document._eventListeners && document._eventListeners['mousemove']) {
            for (var i = 0; i < document._eventListeners['mousemove'].length; i++) {
                try {
                    document._eventListeners['mousemove'][i].call(document, mouseEvent);
                } catch(e) {}
            }
        }
    },

    // 恢复 process 对象（供需要时使用）
    restoreProcess: function() {
        if (global._process) {
            global.process = global._process;
        }
    }
};
