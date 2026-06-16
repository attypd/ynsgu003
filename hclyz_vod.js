var HOST = "http://api.hclyz.com:81";

function init(cfg) {}

// 1. 首页分类：完整提取自图片 1000070914、1000070916、1000070917
function home(filter) {
    var classes = [
        // 图片 1000070914 包含的平台
        {"type_id": "jsonmimi.txt", "type_name": "咪咪"},
        {"type_id": "jsonjiaomei.txt", "type_name": "娇媚"},
        {"type_id": "jsonhuanggua.txt", "type_name": "黄瓜"},
        {"type_id": "jsonsequ.txt", "type_name": "色趣"},
        {"type_id": "jsonnuomi.txt", "type_name": "糯米"},
        {"type_id": "jsonxiaomifeng.txt", "type_name": "小蜜蜂"},
        {"type_id": "jsonxiaohongmao.txt", "type_name": "小红帽"},
        {"type_id": "jsontaohuayun.txt", "type_name": "桃花运"},
        {"type_id": "jsonkugua.txt", "type_name": "苦瓜"},
        {"type_id": "jsonaiaini.txt", "type_name": "爱爱你"},
        {"type_id": "jsonyinghuayui.txt", "type_name": "樱花雨i"},
        
        // 图片 1000070916 包含的平台
        {"type_id": "jsonjinyu.txt", "type_name": "金鱼"},
        {"type_id": "jsontaohua.txt", "type_name": "桃花"},
        {"type_id": "jsonhuafang.txt", "type_name": "花房"},
        {"type_id": "jsonxiaoxiannu.txt", "type_name": "小仙女"},
        {"type_id": "jsonshijuexiu.txt", "type_name": "视觉秀"},
        {"type_id": "jsonxiaotianshi.txt", "type_name": "小天使"},
        {"type_id": "jsonyizhibo.txt", "type_name": "一直播"},
        {"type_id": "jsoncaiyun.txt", "type_name": "彩云"},
        {"type_id": "jsonanyu.txt", "type_name": "暗语"},
        
        // 图片 1000070917 包含的平台
        {"type_id": "jsoncaihong.txt", "type_name": "彩虹"},
        {"type_id": "jsonjiujiu.txt", "type_name": "久久"},
        {"type_id": "jsonyami.txt", "type_name": "亚米"},
        {"type_id": "jsondielian.txt", "type_name": "蝶恋"},
        {"type_id": "jsonyeyaoji.txt", "type_name": "夜妖姬"},
        {"type_id": "jsontaolu.txt", "type_name": "套路"},
        {"type_id": "jsonyinghua.txt", "type_name": "樱花"},
        {"type_id": "jsonxiangse.txt", "type_name": "享色"},
        {"type_id": "jsonhonglangman.txt", "type_name": "红浪漫"}
    ];
    return JSON.stringify({ class: classes });
}

function homeVod() {
    return JSON.stringify({ list: [] });
}

// 2. 核心逻辑：加载对应分类时，把接口数据实时转换成带主播图片的海报卡片
function category(tid, pg, filter, extend) {
    try {
        var url = HOST + "/mf/" + tid;
        var res = req(url, {
            headers: {
                "User-Agent": "Mozilla/5.0 (Linux; Android 15; Mobile)"
            }
        });
        
        var json = JSON.parse(res.content.trim());
        var list = [];
        var zhubo = json.zhubo || [];

        for (var i = 0; i < zhubo.length; i++) {
            var item = zhubo[i];
            // 提取主播头像作为海报墙图片，若没有则使用默认直播占位图
            var picUrl = item.img || item.pic || item.head || "https://img.icons8.com/color/96/live-video.png";
            
            list.push({
                "vod_id": item.address, 
                "vod_name": item.title || ("房间_" + (i + 1)),
                "vod_pic": picUrl, 
                "vod_remarks": "🟢 正在直播"
            });
        }

        return JSON.stringify({
            page: 1,
            pagecount: 1,
            limit: list.length,
            total: list.length,
            list: list
        });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

// 3. 点击卡片进入详情页
function detail(id) {
    var vod = {
        "vod_id": id,
        "vod_name": "直播间详情",
        "vod_play_from": "高清极速直播",
        "vod_play_url": "点击播放$" + id
    };
    return JSON.stringify({ list: [vod] });
}

// 4. 点击播放时输出实时流地址
function play(flag, id, flags) {
    return JSON.stringify({
        parse: 0,
        url: id
    });
}

function search(wd, quick) {
    return JSON.stringify({ list: [] });
}

export default {
    meta: { key: 'hclyz_vod', name: '图片直播点播', type: 3 },
    init: init, home: home, homeVod: homeVod, category: category, detail: detail, play: play, search: search
};
