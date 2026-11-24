import json
import requests

BASE_URL = "http://api.hclyz.com:81/mf/"
DEFAULT_PIC = "https://img.icons8.com/color/96/live-video.png"

RAW_PLATFORMS = [
    ("卡哇伊", "jsonkawayi.txt"),
    ("咪狐", "jsonmihu.txt"),
    ("花蝴蝶", "jsonhuahudie.txt"),
    ("蜜桃", "jsonmitao.txt"),
    ("番茄社区", "jsonfanjiashequ.txt"),
    ("LOVE", "jsonLOVE.txt"),
    ("小妲己", "jsonxiaodaji.txt"),
    ("77直播", "json77zhibo.txt"),
    ("依依", "jsonyiyi.txt"),
    ("日出", "jsonrichu.txt"),
    ("彩虹", "jsoncaihong.txt"),
    ("久久", "jsonjiujiu.txt"),
    ("亚米", "jsonyami.txt"),
    ("蝶恋", "jsondielian.txt"),
    ("夜妖姬", "jsonyeyaoji.txt"),
    ("套路", "jsontaolu.txt"),
    ("樱花", "jsonyinghua.txt"),
    ("享色", "jsonxiangse.txt"),
    ("红浪漫", "jsonhonglangman.txt"),
    ("金鱼", "jsonjinyu.txt"),
    ("桃花", "jsontaohua.txt"),
    ("花房", "jsonhuafang.txt"),
    ("小仙女", "jsonxiaoxiannu.txt"),
    ("视觉秀", "jsonshijuexiu.txt"),
    ("小天使", "jsonxiaotianshi.txt"),
    ("一直播", "jsonyizhibo.txt"),
    ("彩云", "jsoncaiyun.txt"),
    ("暗语", "jsonanyu.txt"),
    ("咪咪", "jsonmimi.txt"),
    ("娇媚", "jsonjiaomei.txt"),
    ("黄瓜", "jsonhuanggua.txt"),
    ("色趣", "jsonsequ.txt"),
    ("糯米", "jsonnuomi.txt"),
    ("小蜜蜂", "jsonxiaomifeng.txt"),
    ("小红帽", "jsonxiaohongmao.txt"),
    ("桃花运", "jsontaohuayun.txt"),
    ("苦瓜", "jsonkugua.txt"),
    ("爱爱你", "jsonaiaini.txt"),
    ("樱花雨i", "jsonyinghuayui.txt"),
    ("盘他", "jsonpanta.txt"),
    ("夜色", "jsonyese.txt"),
    ("蝴蝶", "jsonhudie.txt"),
    ("小天仙", "jsonxiaotianxian.txt"),
    ("杏趣", "jsonxingqu.txt"),
    ("小坏蛋", "jsonxiaohuaidan.txt"),
    ("飘雪", "jsonpiaoxue.txt"),
    ("樱桃", "jsonyingtao.txt"),
    ("奥斯卡", "jsonaosika.txt"),
    ("卡路里", "jsonkaluli.txt"),
    ("红高粱", "jsonhonggaoliang.txt"),
    ("付宝", "jsonfubao.txt"),
    ("小黄书", "jsonxiaohuangshu.txt"),
    ("二嫂", "jsonersao.txt"),
    ("花果山", "jsonhuaguoshan.txt"),
    ("云鹿", "jsonyunlu.txt"),
    ("菠萝", "jsonboluo.txt"),
    ("星宝贝", "jsonxingbaobei.txt"),
    ("夜艳", "jsonyeyan.txt"),
    ("七仙女s", "jsonqixiannus.txt"),
    ("夜来香", "jsonyelaixiang.txt"),
    ("爱零", "jsonailing.txt"),
    ("十八禁", "jsonshibajin.txt"),
    ("兰桂坊", "jsonlanguifang.txt"),
    ("Dancelife", "jsonDancelife.txt"),
    ("小萌猪", "jsonxiaomengzhu.txt"),
    ("蝴蝶飞", "jsonhudiefei.txt"),
    ("幽梦", "jsonyoumeng.txt"),
    ("丽柜厅", "jsonliguiting.txt"),
    ("蛟龙", "jsonjiaolong.txt"),
    ("颜如玉", "jsonyanruyu.txt"),
    ("橙秀", "jsonchengxiu.txt"),
    ("豹娱l", "jsonbaoyul.txt"),
    ("小花螺", "jsonxiaohualuo.txt"),
    ("皇后", "jsonhuanghou.txt"),
    ("心之恋", "jsonxinzhilian.txt"),
    ("台妹l", "jsontaimeil.txt"),
    ("爱恋", "jsonailian.txt"),
    ("903娱乐", "json903yule.txt"),
    ("九尾狐", "jsonjiuweihu.txt"),
    ("尤物岛", "jsonyouwudao.txt"),
    ("坦克", "jsontanke.txt"),
    ("好基友", "jsonhaojiyou.txt"),
    ("夜女郎", "jsonyenulang.txt"),
    ("娇喘", "jsonjiaochuan.txt"),
    ("芒果派", "jsonmangguopai.txt"),
    ("媚颜", "jsonmeiyan.txt"),
    ("风流", "jsonfengliu.txt"),
    ("夜律", "jsonyelu.txt"),
    ("玲珑", "jsonlinglong.txt"),
    ("浴火", "jsonyuhuo.txt"),
    ("翠鸟", "jsoncuiniao.txt"),
    ("幸运星", "jsonxingyunxing.txt"),
    ("她秀", "jsontaxiu.txt"),
    ("招财猫", "jsonzhaocaimao.txt"),
    ("双碟", "jsonshuangdie.txt"),
    ("糖果", "jsontangguo.txt"),
    ("么么哒", "jsonmemeda.txt"),
    ("小性感", "jsonxiaoxinggan.txt"),
    ("小喵宠", "jsonxiaomiaochong.txt"),
    ("兔女郎", "jsontunulang.txt"),
    ("睡美人", "jsonshuimeiren.txt"),
    ("金呗", "jsonjinbei.txt"),
    ("美夕", "jsonmeixi.txt"),
    ("小妖", "jsonxiaoyao.txt"),
    ("约直播", "jsonyuezhibo.txt"),
    ("花仙子", "jsonhuaxianzi.txt"),
    ("土豪", "jsontuhao.txt"),
    ("红妆", "jsonhongzhuang.txt"),
    ("妞妞", "jsonniuniu.txt"),
    ("艳后", "jsonyanhou.txt"),
    ("moon", "jsonmoon.txt"),
    ("蓝猫", "jsonlanmao.txt"),
    ("美人妆", "jsonmeirenzhuang.txt"),
    ("入巷", "jsonruxiang.txt"),
    ("持久男", "jsonchijiunan.txt"),
    ("倾心", "jsonqingxin.txt"),
    ("小精灵", "jsonxiaojingling.txt"),
    ("偶遇", "jsonouyu.txt"),
    ("灰灰", "jsonhuihui.txt"),
    ("猫头鹰", "jsonmaotouying.txt"),
    ("喜欢你", "jsonxihuanni.txt"),
    ("夜纯", "jsonyechun.txt"),
    ("杏播", "jsonxingbo.txt"),
    ("名流", "jsonmingliu.txt"),
    ("小辣椒", "jsonxiaolajiao.txt"),
    ("蚊香社", "jsonwenxiangshe.txt"),
    ("牵手", "jsonqianshou.txt"),
    ("情趣", "jsonqingqu.txt"),
    ("蓝月亮", "jsonlanyueliang.txt"),
    ("小棉袄", "jsonxiaomianao.txt"),
]


def get_unique_platforms():
    seen_names = set()
    seen_files = set()
    result = []
    for name, filename in RAW_PLATFORMS:
        if name in seen_names or filename in seen_files:
            continue
        seen_names.add(name)
        seen_files.add(filename)
        result.append((name, filename))
    return result


def clean_text(val, fallback):
    s = str(val or "").strip().replace(",", " ").replace("\n", " ")
    return s if s else fallback


def fetch_all():
    headers = {"User-Agent": "Mozilla/5.0"}
    classes = [{"type_id": "hot", "type_name": "🔥 热门推荐"}]
    vod_list = []
    hot_list = []

    platforms = get_unique_platforms()
    for idx_p, (name, filename) in enumerate(platforms, start=1):
        type_id = f"p_{idx_p}"
        classes.append({"type_id": type_id, "type_name": name})

        url = f"{BASE_URL}{filename}"
        try:
            resp = requests.get(url, headers=headers, timeout=6)
            resp.raise_for_status()
            payload = resp.json()
        except Exception:
            continue

        zhubo = payload.get("zhubo")
        if not isinstance(zhubo, list):
            continue

        seen_addr = set()
        plat_count = 0

        for idx_r, room in enumerate(zhubo, start=1):
            if not isinstance(room, dict):
                continue
            addr = str(room.get("address") or "").strip()
            if not addr.startswith(("http://", "https://", "rtmp://")):
                continue
            if addr in seen_addr:
                continue
            seen_addr.add(addr)

            title = clean_text(room.get("title"), f"{name}_{idx_r}")
            pic = str(room.get("img") or room.get("pic") or room.get("head") or "").strip()
            if not pic.startswith(("http://", "https://")):
                pic = DEFAULT_PIC

            vod_item = {
                "vod_id": f"{type_id}_{idx_r}",
                "vod_name": title,
                "vod_pic": pic,
                "type_id": type_id,
                "type_name": name,
                "vod_remarks": name,
                "vod_play_from": "直播源",
                "vod_play_url": f"{title}${addr}",
            }
            vod_list.append(vod_item)

            if plat_count < 2 and len(hot_list) < 24:
                hot_item = {
                    "vod_id": f"hot_{idx_p}_{idx_r}",
                    "vod_name": title,
                    "vod_pic": pic,
                    "type_id": "hot",
                    "type_name": "🔥 热门推荐",
                    "vod_remarks": f"🔥 {name}",
                    "vod_play_from": "直播源",
                    "vod_play_url": f"{title}${addr}",
                }
                hot_list.append(hot_item)

            plat_count += 1

    final_list = hot_list + vod_list
    output = {
        "code": 1,
        "msg": "数据列表",
        "page": 1,
        "pagecount": 1,
        "limit": len(final_list),
        "total": len(final_list),
        "class": classes,
        "list": final_list,
    }

    with open("hclyz_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fetch_all()
