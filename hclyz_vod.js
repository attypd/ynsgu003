var HOST = "http://api.hclyz.com:81";

function init(cfg) {}

// 首页分类：全量合并你发给我的所有图片里的平台标签
function home(filter) {
    var classes = [
        // === 第一批图片遗漏的王牌平台 ===
        {"type_id": "jsonkawayi.txt", "type_name": "卡哇伊"},
        {"type_id": "jsonmihu.txt", "type_name": "咪狐"},
        {"type_id": "jsonhuahudie.txt", "type_name": "花蝴蝶"},
        {"type_id": "jsonmitao.txt", "type_name": "蜜桃"},
        {"type_id": "jsonfanjiashequ.txt", "type_name": "番茄社区"},
        {"type_id": "jsonLOVE.txt", "type_name": "LOVE"},
        {"type_id": "jsonxiaodaji.txt", "type_name": "小妲己"},
        {"type_id": "json77zhibo.txt", "type_name": "77直播"},
        {"type_id": "jsonyiyi.txt", "type_name": "依依"},
        {"type_id": "jsonrichu.txt", "type_name": "日出"},
        {"type_id": "jsonchijiunan.txt", "type_name": "持久男"},
        {"type_id": "jsonqingxin.txt", "type_name": "倾心"},
        {"type_id": "jsonxiaojingling.txt", "type_name": "小精灵"},
        {"type_id": "jsonouyu.txt", "type_name": "偶遇"},
        {"type_id": "jsonhuihui.txt", "type_name": "灰灰"},
        {"type_id": "jsonmaotouying.txt", "type_name": "猫头鹰"},
        {"type_id": "jsonxihuanni.txt", "type_name": "喜欢你"},
        {"type_id": "jsonyechun.txt", "type_name": "夜纯"},
        {"type_id": "jsonxingbo.txt", "type_name": "杏播"},
        {"type_id": "jsonmingliu.txt", "type_name": "名流"},
        {"type_id": "jsonxialajiao.txt", "type_name": "小辣椒"},
        {"type_id": "jsonwenxiangshe.txt", "type_name": "蚊香社"},
        {"type_id": "jsonqianshou.txt", "type_name": "牵手"},
        {"type_id": "jsonqingqu.txt", "type_name": "情趣"},
        {"type_id": "jsonyuezhibo.txt", "type_name": "约直播"},
        {"type_id": "jsonhuaxianzi.txt", "type_name": "花仙子"},
        {"type_id": "jsontuhao.txt", "type_name": "土豪"},
        {"type_id": "jsonhongzhuang.txt", "type_name": "红妆"},
        {"type_id": "jsonniuniu.txt", "type_name": "妞妞"},
        {"type_id": "jsonyanhou.txt", "type_name": "艳后"},
        {"type_id": "jsonmoon.txt", "type_name": "moon"},
        {"type_id": "jsonlanmao.txt", "type_name": "蓝猫"},
        {"type_id": "jsonmeirenzhuang.txt", "type_name": "美人妆"},
        {"type_id": "jsonruxiang.txt", "type_name": "入巷"},
        {"type_id": "jsonshuangdie.txt", "type_name": "双碟"},
        {"type_id": "jsontangguo.txt", "type_name": "糖果"},
        {"type_id": "jsonmemeda.txt", "type_name": "么么哒"},
        {"type_id": "jsonxiaoxinggan.txt", "type_name": "小性感"},
        {"type_id": "jsonxiaomiaochong.txt", "type_name": "小喵宠"},
        {"type_id": "jsontunulang.txt", "type_name": "兔女郎"},
        {"type_id": "jsonshuimeiren.txt", "type_name": "睡美人"},
        {"type_id": "jsonjinbei.txt", "type_name": "金呗"},
        {"type_id": "jsonmeixi.txt", "type_name": "美夕"},
        {"type_id": "jsonxiaoyao.txt", "type_name": "小妖"},
        {"type_id": "jsonjiaochuan.txt", "type_name": "娇喘"},
        {"type_id": "jsonmangguopai.txt", "type_name": "芒果派"},
        {"type_id": "jsonmeiyan.txt", "type_name": "媚颜"},
        {"type_id": "jsonfengliu.txt", "type_name": "风流"},
        {"type_id": "jsonyelu.txt", "type_name": "夜律"},
        {"type_id": "jsonlinglong.txt", "type_name": "玲珑"},
        {"type_id": "jsonyuhuo.txt", "type_name": "浴火"},
        {"type_id": "jsoncuiniao.txt", "type_name": "翠鸟"},
        {"type_id": "jsonxingyunxing.txt", "type_name": "幸运星"},
        {"type_id": "jsontaxiu.txt", "type_name": "她秀"},
        {"type_id": "jsonzhaocaimao.txt", "type_name": "招财猫"},
        {"type_id": "jsonoumeiTRANS.txt", "type_name": "欧美TRANS"},
        {"type_id": "jsontaimeil.txt", "type_name": "台妹"},
        {"type_id": "jsonailian.txt", "type_name": "爱恋"},
        {"type_id": "json903yule.txt", "type_name": "903娱乐"},
        {"type_id": "jsonjiuweihu.txt", "type_name": "九尾狐"},
        {"type_id": "jsonyouwudao.txt", "type_name": "尤物岛"},
        {"type_id": "jsontanke.txt", "type_name": "坦克"},
        {"type_id": "jsonhaojiyou.txt", "type_name": "好基友"},
        {"type_id": "jsonyenulang.txt", "type_name": "夜女郎"},
        {"type_id": "jsonjiaolong.txt", "type_name": "蛟龙"},
        {"type_id": "jsonyanruyu.txt", "type_name": "颜如玉"},
        {"type_id": "jsonchengxi.txt", "type_name": "橙秀"},
        {"type_id": "jsonbaoyul.txt", "type_name": "豹娱"},
        {"type_id": "jsonxiaohualuo.txt", "type_name": "小花螺"},
        {"type_id": "jsonhuanghou.txt", "type_name": "皇后"},
        {"type_id": "jsonxinzhilian.txt", "type_name": "心之恋"},
        {"type_id": "jsonoumeiFEATURED.txt", "type_name": "欧美FEATURED"},
        {"type_id": "jsonoumeiFEMALE.txt", "type_name": "欧美FEMALE"},
        {"type_id": "jsonoumeiMALE.txt", "type_name": "欧美MALE"},
        {"type_id": "jsonoumeiCOUPLE.txt", "type_name": "欧美COUPLE"},
        {"type_id": "jsonqixiannus.txt", "type_name": "七仙女s"},
        {"type_id": "jsonyelaixiang.txt", "type_name": "夜来香"},
        {"type_id": "jsonailing.txt", "type_name": "爱零"},
        {"type_id": "jsonshibajin.txt", "type_name": "十八禁"},
        {"type_id": "jsonlanguifang.txt", "type_name": "兰桂坊"},
        {"type_id": "jsonDancelife.txt", "type_name": "Dancelife"},
        {"type_id": "jsonxiaomengzhu.txt", "type_name": "小萌猪"},
        {"type_id": "jsonhudiefei.txt", "type_name": "蝴蝶飞"},
        {"type_id": "jsonyoumeng.txt", "type_name": "幽梦"},
        {"type_id": "jsonliguiting.txt", "type_name": "丽柜厅"},
        {"type_id": "jsonaosika.txt", "type_name": "奥斯卡"},
        {"type_id": "jsonkaluli.txt", "type_name": "卡路里"},
        {"type_id": "jsonhonggaoliang.txt", "type_name": "红高粱"},
        {"type_id": "jsonfubao.txt", "type_name": "付宝"},
        {"type_id": "jsonxiaohuangshu.txt", "type_name": "小黄书"},
        {"type_id": "jsonersao.txt", "type_name": "二嫂"},
        {"type_id": "jsonhuaguoshan.txt", "type_name": "花果山"},
        {"type_id": "jsonyunlu.txt", "type_name": "云鹿"},
        {"type_id": "jsonboluo.txt", "type_name": "菠萝"},
        {"type_id": "jsonxingbaobei.txt", "type_name": "星宝贝"},
        {"type_id": "jsonyeyan.txt", "type_name": "夜艳"},
        {"type_id": "jsonpanta.txt", "type_name": "盘他"},
        {"type_id": "jsonyese.txt", "type_name": "夜色"},
        {"type_id": "jsonhudie.txt", "type_name": "蝴蝶"},
        {"type_id": "jsonxiaotianxian.txt", "type_name": "小天仙"},
        {"type_id": "jsonxingqu.txt", "type_name": "杏趣"},
        {"type_id": "jsonxiaohuaidan.txt", "type_name": "小坏蛋"},
        {"type_id": "jsonpiaoxue.txt", "type_name": "飘雪"},
        {"type_id": "jsonyingtao.txt", "type_name": "樱桃"},

        // === 第二批图片里的平台 ===
        {"type_id": "jsonmimi.txt", "type_name": "咪咪"},
        {"type_id": "jsonjiaomei.txt", "type_name": "娇媚"},
        {"type_id": "jsonhuanggua.txt", "type_name": "黄瓜"},
        {"type_id": "jsonsequ.txt", "type_name": "色趣"},
        {"type_id": "jsonnuomi.txt", "type_name": "糯米"},
        {"type_id": "jsonxiaomifeng.txt", "type_name": "小蜜蜂"},
        {"type_id": "jsonxiaohongmao.txt", "type_name": "小红帽"},
        {"type_id": "jsontahuayun.txt", "type_name": "桃花运"},
        {"type_id": "jsonkugua.txt", "type_name": "苦瓜"},
        {"type_id": "jsonaiaini.txt", "type_name": "爱爱你"},
        {"type_id": "jsonyinghuayui.txt", "type_name": "樱花雨i"},
        {"type_id": "jsonjinyu.txt", "type_name": "金鱼"},
        {"type_id": "jsontaohua.txt", "type_name": "桃花"},
        {"type_id": "jsonhuafang.txt", "type_name": "花房"},
        {"type_id": "jsonxiaoxiannu.txt", "type_name": "小仙女"},
        {"type_id": "jsonshijuexiu.txt", "type_name": "视觉秀"},
        {"type_id": "jsonxiaotianshi.txt", "type_name": "小天使"},
        {"type_id": "jsonyizhibo.txt", "type_name": "一直播"},
        {"type_id": "jsoncaiyun.txt", "type_name": "彩云"},
        {"type_id": "jsonanyu.txt", "type_name": "暗语"},
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
            var picUrl = item.img || item.pic || item.head || "https://img.icons8.com/color/96/live-video.png";
            
            list.push({
                "vod_id": item.address, 
                "vod_name": item.title || ("房间_" + (i + 1)),
                "vod_pic": picUrl, 
                "vod_remarks": "🟢 正在直播"
            });
        }

        return JSON.stringify({
            page: 1, pagecount: 1, limit: list.length, total: list.length, list: list
        });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

function detail(id) {
    var vod = {
        "vod_id": id,
        "vod_name": "直播间详情",
        "vod_play_from": "高清极速直播",
        "vod_play_url": "点击播放$" + id
    };
    return JSON.stringify({ list: [vod] });
}

function play(flag, id, flags) {
    return JSON.stringify({ parse: 0, url: id });
}

function search(wd, quick) {
    return JSON.stringify({ list: [] });
}

export default {
    meta: { key: 'hclyz_vod', name: '图片直播点播', type: 3 },
    init: init, home: home, homeVod: homeVod, category: category, detail: detail, play: play, search: search
};
