var BASE_RAW = "https://gh-proxy.org/https://raw.githubusercontent.com/attypd/ynsgu003/main/data/";

function init(cfg) {}

function home(filter) {
    var classes = [
        {"type_id": "RECOMMEND", "type_name": "🔥 热门推荐"},
        {"type_id": "jsonkawayi.json", "type_name": "卡哇伊"},
        {"type_id": "jsonmihu.json", "type_name": "咪狐"},
        {"type_id": "jsonhuahudie.json", "type_name": "花蝴蝶"},
        {"type_id": "jsonmitao.json", "type_name": "蜜桃"},
        {"type_id": "jsonfanjiashequ.json", "type_name": "番茄社区"},
        {"type_id": "jsonLOVE.json", "type_name": "LOVE"},
        {"type_id": "jsonxiaodaji.json", "type_name": "小妲己"},
        {"type_id": "json77zhibo.json", "type_name": "77直播"},
        {"type_id": "jsonyiyi.json", "type_name": "依依"},
        {"type_id": "jsonrichu.json", "type_name": "日出"},
        {"type_id": "jsonchijiunan.json", "type_name": "持久男"},
        {"type_id": "jsonqingxin.json", "type_name": "倾心"},
        {"type_id": "jsonxiaojingling.json", "type_name": "小精灵"},
        {"type_id": "jsonouyu.json", "type_name": "偶遇"},
        {"type_id": "jsonhuihui.json", "type_name": "灰灰"},
        {"type_id": "jsonmaotouying.json", "type_name": "猫头鹰"},
        {"type_id": "jsonxihuanni.json", "type_name": "喜欢你"},
        {"type_id": "jsonyechun.json", "type_name": "夜纯"},
        {"type_id": "jsonxingbo.json", "type_name": "杏播"},
        {"type_id": "jsonmingliu.json", "type_name": "名流"},
        {"type_id": "jsonxiaolajiao.json", "type_name": "小辣椒"},
        {"type_id": "jsonwenxiangshe.json", "type_name": "蚊香社"},
        {"type_id": "jsonqianshou.json", "type_name": "牵手"},
        {"type_id": "jsonqingqu.json", "type_name": "情趣"},
        {"type_id": "jsonyuezhibo.json", "type_name": "约直播"},
        {"type_id": "jsonhuaxianzi.json", "type_name": "花仙子"},
        {"type_id": "jsontuhao.json", "type_name": "土豪"},
        {"type_id": "jsonhongzhuang.json", "type_name": "红妆"},
        {"type_id": "jsonniuniu.json", "type_name": "妞妞"},
        {"type_id": "jsonyanhou.json", "type_name": "艳后"},
        {"type_id": "jsonmoon.json", "type_name": "moon"},
        {"type_id": "jsonlanmao.json", "type_name": "蓝猫"},
        {"type_id": "jsonmeirenzhuang.json", "type_name": "美人妆"},
        {"type_id": "jsonruxiang.json", "type_name": "入巷"},
        {"type_id": "jsonshuangdie.json", "type_name": "双碟"},
        {"type_id": "jsontangguo.json", "type_name": "糖果"},
        {"type_id": "jsonmemeda.json", "type_name": "么么哒"},
        {"type_id": "jsonxiaoxinggan.json", "type_name": "小性感"},
        {"type_id": "jsonxiaomiaochong.json", "type_name": "小喵宠"},
        {"type_id": "jsontunulang.json", "type_name": "兔女郎"},
        {"type_id": "jsonshuimeiren.json", "type_name": "睡美人"},
        {"type_id": "jsonjinbei.json", "type_name": "金呗"},
        {"type_id": "jsonmeixi.json", "type_name": "美夕"},
        {"type_id": "jsonxiaoyao.json", "type_name": "小妖"},
        {"type_id": "jsonjiaochuan.json", "type_name": "娇喘"},
        {"type_id": "jsonmangguopai.json", "type_name": "芒果派"},
        {"type_id": "jsonmeiyan.json", "type_name": "媚颜"},
        {"type_id": "jsonfengliu.json", "type_name": "风流"},
        {"type_id": "jsonyelu.json", "type_name": "夜律"},
        {"type_id": "jsonlinglong.json", "type_name": "玲珑"},
        {"type_id": "jsonyuhuo.json", "type_name": "浴火"},
        {"type_id": "jsoncuiniao.json", "type_name": "翠鸟"},
        {"type_id": "jsonxingyunxing.json", "type_name": "幸运星"},
        {"type_id": "jsontaxiu.json", "type_name": "她秀"},
        {"type_id": "jsonzhaocaimao.json", "type_name": "招财猫"},
        {"type_id": "jsonoumeiTRANS.json", "type_name": "欧美TRANS"},
        {"type_id": "jsontaimeil.json", "type_name": "台妹"},
        {"type_id": "jsonailian.json", "type_name": "爱恋"},
        {"type_id": "json903yule.json", "type_name": "903娱乐"},
        {"type_id": "jsonjiuweihu.json", "type_name": "九尾狐"},
        {"type_id": "jsonyouwudao.json", "type_name": "尤物岛"},
        {"type_id": "jsontanke.json", "type_name": "坦克"},
        {"type_id": "jsonhaojiyou.json", "type_name": "好基友"},
        {"type_id": "jsonyenulang.json", "type_name": "夜女郎"},
        {"type_id": "jsonjiaolong.json", "type_name": "蛟龙"},
        {"type_id": "jsonyanruyu.json", "type_name": "颜如玉"},
        {"type_id": "jsonchengxi.json", "type_name": "橙秀"},
        {"type_id": "jsonbaoyul.json", "type_name": "豹娱"},
        {"type_id": "jsonxiaohualuo.json", "type_name": "小花螺"},
        {"type_id": "jsonhuanghou.json", "type_name": "皇后"},
        {"type_id": "jsonxinzhilian.json", "type_name": "心之恋"},
        {"type_id": "jsonoumeiFEATURED.json", "type_name": "欧美FEATURED"},
        {"type_id": "jsonoumeiFEMALE.json", "type_name": "欧美FEMALE"},
        {"type_id": "jsonoumeiMALE.json", "type_name": "欧美MALE"},
        {"type_id": "jsonoumeiCOUPLE.json", "type_name": "欧美COUPLE"},
        {"type_id": "jsonqixiannus.json", "type_name": "七仙女s"},
        {"type_id": "jsonyelaixiang.json", "type_name": "夜来香"},
        {"type_id": "jsonailing.json", "type_name": "爱零"},
        {"type_id": "jsonshibajin.json", "type_name": "十八禁"},
        {"type_id": "jsonlanguifang.json", "type_name": "兰桂坊"},
        {"type_id": "jsonDancelife.json", "type_name": "Dancelife"},
        {"type_id": "jsonxiaomengzhu.json", "type_name": "小萌猪"},
        {"type_id": "jsonhudiefei.json", "type_name": "蝴蝶飞"},
        {"type_id": "jsonyoumeng.json", "type_name": "幽梦"},
        {"type_id": "jsonliguiting.json", "type_name": "丽柜厅"},
        {"type_id": "jsonaosika.json", "type_name": "奥斯卡"},
        {"type_id": "jsonkaluli.json", "type_name": "卡路里"},
        {"type_id": "jsonhonggaoliang.json", "type_name": "红高粱"},
        {"type_id": "jsonfubao.json", "type_name": "付宝"},
        {"type_id": "jsonxiaohuangshu.json", "type_name": "小黄书"},
        {"type_id": "jsonersao.json", "type_name": "二嫂"},
        {"type_id": "jsonhuaguoshan.json", "type_name": "花果山"},
        {"type_id": "jsonyunlu.json", "type_name": "云鹿"},
        {"type_id": "jsonboluo.json", "type_name": "菠萝"},
        {"type_id": "jsonxingbaobei.json", "type_name": "星宝贝"},
        {"type_id": "jsonyeyan.json", "type_name": "夜艳"},
        {"type_id": "jsonpanta.json", "type_name": "盘他"},
        {"type_id": "jsonyese.json", "type_name": "夜色"},
        {"type_id": "jsonhudie.json", "type_name": "蝴蝶"},
        {"type_id": "jsonxiaotianxian.json", "type_name": "小天仙"},
        {"type_id": "jsonxingqu.json", "type_name": "杏趣"},
        {"type_id": "jsonxiaohuaidan.json", "type_name": "小坏蛋"},
        {"type_id": "jsonpiaoxue.json", "type_name": "飘雪"},
        {"type_id": "jsonyingtao.json", "type_name": "樱桃"},
        {"type_id": "jsonmimi.json", "type_name": "咪咪"},
        {"type_id": "jsonhuanggua.json", "type_name": "黄瓜"},
        {"type_id": "jsonsequ.json", "type_name": "色趣"},
        {"type_id": "jsonnuomi.json", "type_name": "糯米"},
        {"type_id": "jsonxiaomifeng.json", "type_name": "小蜜蜂"},
        {"type_id": "jsonxiaohongmao.json", "type_name": "小红帽"},
        {"type_id": "jsontaohuayun.txt".replace(".txt", ".json"), "type_name": "桃花运"}, // 规范处理
        {"type_id": "jsonkugua.json", "type_name": "苦瓜"},
        {"type_id": "jsonaiaini.json", "type_name": "爱爱你"},
        {"type_id": "jsonyinghuayui.json", "type_name": "樱花雨i"},
        {"type_id": "jsonjinyu.json", "type_name": "金鱼"},
        {"type_id": "jsontaohua.json", "type_name": "桃花"},
        {"type_id": "jsonhuafang.json", "type_name": "花房"},
        {"type_id": "jsonxiaoxiannu.json", "type_name": "小仙女"},
        {"type_id": "jsonshijuexiu.json", "type_name": "视觉秀"},
        {"type_id": "jsonxiaotianshi.json", "type_name": "小天使"},
        {"type_id": "jsonyizhibo.json", "type_name": "一直播"},
        {"type_id": "jsoncaiyun.json", "type_name": "彩云"},
        {"type_id": "jsonanyu.json", "type_name": "暗语"},
        {"type_id": "jsoncaihong.json", "type_name": "彩虹"},
        {"type_id": "jsonjiujiu.json", "type_name": "久久"},
        {"type_id": "jsonyami.json", "type_name": "亚米"},
        {"type_id": "jsondielian.json", "type_name": "蝶恋"},
        {"type_id": "jsonyeyaoji.json", "type_name": "夜妖姬"},
        {"type_id": "jsontaolu.json", "type_name": "套路"},
        {"type_id": "jsonyinghua.json", "type_name": "樱花"},
        {"type_id": "jsonxiangse.json", "type_name": "享色"},
        {"type_id": "jsonhonglangman.json", "type_name": "红浪漫"}
    ];
    return JSON.stringify({ class: classes });
}

function homeVod() {
    try {
        var url = BASE_RAW + "jsonkawayi.json";
        var res = req(url, { headers: { "User-Agent": "Mozilla/5.0" } });
        var json = JSON.parse(res.content.trim());
        var list = [];
        var zhubo = json.zhubo || [];
        for (var i = 0; i < Math.min(zhubo.length, 12); i++) {
            var item = zhubo[i];
            list.push({
                "vod_id": item.address || "",
                "vod_name": (item.title || "推荐主播").trim().replace(",", ""),
                "vod_pic": item.img || item.pic || "https://img.icons8.com/color/96/live-video.png",
                "vod_remarks": "🔥 热门推荐"
            });
        }
        return JSON.stringify({ list: list });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

function category(tid, pg, filter, extend) {
    try {
        var list = [];
        if (tid === "RECOMMEND") {
            return homeVod();
        }
        var url = BASE_RAW + tid;
        var res = req(url, { headers: { "User-Agent": "Mozilla/5.0" } });
        var json = JSON.parse(res.content.trim());
        var zhubo = json.zhubo || [];

        for (var i = 0; i < zhubo.length; i++) {
            var item = zhubo[i];
            var picUrl = item.img || item.pic || item.head || "https://img.icons8.com/color/96/live-video.png";
            var title = item.title ? item.title.trim().replace(",", "") : ("房间_" + (i + 1));
            var address = item.address || "";
            
            if (address) {
                list.push({
                    "vod_id": address,
                    "vod_name": title,
                    "vod_pic": picUrl,
                    "vod_remarks": "🟢 直播中"
                });
            }
        }

        return JSON.stringify({
            page: 1, pagecount: 1, limit: list.length, total: list.length, list: list
        });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

function detail(id) {
    return JSON.stringify({ list: [{"vod_id": id, "vod_name": "直播间详情", "vod_play_from": "高清极速直播", "vod_play_url": "点击播放$" + id}] });
}

function play(flag, id, flags) {
    return JSON.stringify({ parse: 0, url: id });
}

function search(wd, quick) {
    return JSON.stringify({ list: [] });
}

export default {
    meta: { key: 'hclyz_vod_smart', name: '智能分平台直播', type: 3 },
    init: init, home: home, homeVod: homeVod, category: category, detail: detail, play: play, search: search
};
