import requests
import json
import os

BASE_URL = "http://api.hclyz.com:81/mf/"

# 从图片提取的完整平台映射
PLATFORMS = {
    "卡哇伊": "jsonkawayi.txt", "咪狐": "jsonmihu.txt", "花蝴蝶": "jsonhuahudie.txt",
    "蜜桃": "jsonmitao.txt", "番茄社区": "jsonfanjiashequ.txt", "LOVE": "jsonLOVE.txt",
    "小妲己": "jsonxiaodaji.txt", "77直播": "json77zhibo.txt", "依依": "jsonyiyi.txt",
    "日出": "jsonrichu.txt", "持久男": "jsonchijiunan.txt", "倾心": "jsonqingxin.txt",
    "小精灵": "jsonxiaojingling.txt", "偶遇": "jsonouyu.txt", "灰灰": "jsonhuihui.txt",
    "猫头鹰": "jsonmaotouying.txt", "喜欢你": "jsonxihuanni.txt", "夜纯": "jsonyechun.txt",
    "杏播": "jsonxingbo.txt", "名流": "jsonmingliu.txt", "小辣椒": "jsonxiaolajiao.txt",
    "蚊香社": "jsonwenxiangshe.txt", "牵手": "jsonqianshou.txt", "情趣": "jsonqingqu.txt",
    "约直播": "jsonyuezhibo.txt", "花仙子": "jsonhuaxianzi.txt", "土豪": "jsontuhao.txt",
    "红妆": "jsonhongzhuang.txt", "妞妞": "jsonniuniu.txt", "艳后": "jsonyanhou.txt",
    "moon": "jsonmoon.txt", "蓝猫": "jsonlanmao.txt", "美人妆": "jsonmeirenzhuang.txt",
    "入巷": "jsonruxiang.txt", "双碟": "jsonshuangdie.txt", "糖果": "jsontangguo.txt",
    "么么哒": "jsonmemeda.txt", "小性感": "jsonxiaoxinggan.txt", "小喵宠": "jsonxiaomiaochong.txt",
    "兔女郎": "jsontunulang.txt", "睡美人": "jsonshuimeiren.txt", "金呗": "jsonjinbei.txt",
    "美夕": "jsonmeixi.txt", "小妖": "jsonxiaoyao.txt", "娇喘": "jsonjiaochuan.txt",
    "芒果派": "jsonmangguopai.txt", "媚颜": "jsonmeiyan.txt", "风流": "jsonfengliu.txt",
    "夜律": "jsonyelu.txt", "玲珑": "jsonlinglong.txt", "浴火": "jsonyuhuo.txt",
    "翠鸟": "jsoncuiniao.txt", "幸运星": "jsonxingyunxing.txt", "她秀": "jsontaxiu.txt",
    "招财猫": "jsonzhaocaimao.txt", "欧美TRANS": "jsonoumeiTRANS.txt", "台妹l": "jsontaimeil.txt",
    "爱恋": "jsonailian.txt", "903娱乐": "json903yule.txt", "九尾狐": "jsonjiuweihu.txt",
    "尤物岛": "jsonyouwudao.txt", "坦克": "jsontanke.txt", "好基友": "jsonhaojiyou.txt",
    "夜女郎": "jsonyenulang.txt", "蛟龙": "jsonjiaolong.txt", "颜如玉": "jsonyanruyu.txt",
    "橙秀": "jsonchengxiu.txt", "豹娱l": "jsonbaoyul.txt", "小花螺": "jsonxiaohualuo.txt",
    "皇后": "jsonhuanghou.txt", "心之恋": "jsonxinzhilian.txt", "欧美FEATURED": "jsonoumeiFEATURED.txt",
    "欧美FEMALE": "jsonoumeiFEMALE.txt", "欧美MALE": "jsonoumeiMALE.txt", "欧美COUPLE": "jsonoumeiCOUPLE.txt",
    "七仙女s": "jsonqixiannus.txt", "夜来香": "jsonyelaixiang.txt", "爱零": "jsonailing.txt",
    "十八禁": "jsonshibajin.txt", "兰桂坊": "jsonlanguifang.txt", "Dancelife": "jsonDancelife.txt",
    "小萌猪": "jsonxiaomengzhu.txt", "蝴蝶飞": "jsonhudiefei.txt", "幽梦": "jsonyoumeng.txt",
    "丽柜厅": "jsonliguiting.txt", "奥斯卡": "jsonaosika.txt", "卡路里": "jsonkaluli.txt",
    "红高粱": "jsonhonggaoliang.txt", "付宝": "jsonfubao.txt", "小黄书": "jsonxiaohuangshu.txt",
    "二嫂": "jsonersao.txt", "花果山": "jsonhuaguoshan.txt", "云鹿": "jsonyunlu.txt",
    "菠萝": "jsonboluo.txt", "星宝贝": "jsonxingbaobei.txt", "夜艳": "jsonyeyan.txt",
    "樱花雨i": "jsonyinghuayui.txt", "盘他": "jsonpanta.txt", "夜色": "jsonyese.txt",
    "蝴蝶": "jsonhudie.txt", "小天仙": "jsonxiaotianxian.txt", "杏趣": "jsonxingqu.txt",
    "小坏蛋": "jsonxiaohuaidan.txt", "飘雪": "jsonpiaoxue.txt", "樱桃": "jsonyingtao.txt",
    "咪咪": "jsonmimi.txt", "黄瓜": "jsonhuanggua.txt", "色趣": "jsonsequ.txt",
    "糯米": "jsonnuomi.txt", "小蜜蜂": "jsonxiaomifeng.txt", "小红帽": "jsonxiaohongmao.txt",
    "桃花运": "jsontahuayun.txt", "苦瓜": "jsonkugua.txt", "爱爱你": "jsonaiaini.txt",
    "金鱼": "jsonjinyu.txt", "桃花": "jsontaohua.txt", "花房": "jsonhuafang.txt",
    "小仙女": "jsonxiaoxiannu.txt", "视觉秀": "jsonshijuexiu.txt", "小天使": "jsonxiaotianshi.txt",
    "一直播": "jsonyizhibo.txt", "彩云": "jsoncaiyun.txt", "暗语": "jsonanyu.txt",
    "彩虹": "jsoncaihong.txt", "久久": "jsonjiujiu.txt", "亚米": "jsonyami.txt",
    "蝶恋": "jsondielian.txt", "夜妖姬": "jsonyeyaoji.txt", "套路": "jsontaolu.txt",
    "樱花": "jsonyinghua.txt", "享色": "jsonxiangse.txt", "红浪漫": "jsonhonglangman.txt"
}

def fetch_all():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.7680.164 Mobile Safari/537.36",
        "Accept-Encoding": "gzip"
    }
    lines = []
    for name, filename in PLATFORMS.items():
        url = f"{BASE_URL}{filename}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                zhubo = data.get("zhubo", [])
                if zhubo:
                    lines.append(f"{name},#genre#")
                    for room in zhubo:
                        title = room.get("title", "房间").strip().replace(",", "")
                        address = room.get("address", "").strip()
                        if address.startswith("http"):
                            lines.append(f"{title},{address}")
                    lines.append("")
        except:
            continue
            
    with open("hclyz_live.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    fetch_all()
