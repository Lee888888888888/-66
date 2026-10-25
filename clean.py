import re
import urllib.request

# 你的所有订阅网址列表（已将你提供的所有网址填入，去掉了注释符号 # 即可直接启用）
URLS = [
    "https://bestcf.pages.dev/xinyitang3/ipv4.txt",
    "https://raw.githubusercontent.com/LancelotRar/best-cf-ips/refs/heads/main/best-cf-ip-collected.txt",
    "https://bestcf.pages.dev/cfyes/ipv4.txt",
    "https://bestcf.pages.dev/s5gy/jp.txt",
    "https://bestcf.pages.dev/s5gy/tw.txt",
    "https://bestcf.pages.dev/tiancheng2/tw.txt",
    "https://bestcf.pages.dev/uouin/all.txt"
]

# 国家/地区关键词映射表（支持全称、简写、中文以及单字母兜底）
REGION_KEYWORDS = {
    "HK": ["HK", "香港", "HONGKONG", "HONG KONG"],
    "TW": ["TW", "台湾", "台灣", "TAIWAN"],
    "MO": ["MO", "澳门", "MACAU"],
    "JP": ["JP", "日本", "JAPAN", "东京", "大阪"],
    "KR": ["KR", "韩国", "首尔", "KOREA"],
    "SG": ["SG", "新加坡", "SINGAPORE"],
    "MY": ["MY", "马来西亚", "MALAYSIA"],
    "TH": ["TH", "泰国", "THAILAND"],
    "VN": ["VN", "越南", "VIETNAM"],
    "PH": ["PH", "菲律宾", "PHILIPPINES"],
    "US": ["US", "美国", "USA", "UNITED STATES"],
    "CA": ["CA", "加拿大", "CANADA"],
    "BR": ["BR", "巴西", "BRAZIL"],
    "GB": ["GB", "UK", "英国", "UNITED KINGDOM"],
    "DE": ["DE", "德国", "GERMANY"],
    "FR": ["FR", "法国", "FRANCE"],
    "NL": ["NL", "荷兰", "NETHERLANDS"],
    "CH": ["CH", "瑞士", "SWITZERLAND"],
    "IT": ["IT", "意大利", "ITALY"],
    "ES": ["ES", "西班牙", "SPAIN"],
    "SE": ["SE", "瑞典", "SWEDEN"],
    "IE": ["IE", "爱尔兰", "IRELAND"],
    "NO": ["NO", "挪威", "NORWAY"],
    "FI": ["FI", "芬兰", "FINLAND"],
    "AU": ["AU", "澳大利亚", "澳洲", "AUSTRALIA"],
    "NZ": ["NZ", "新西兰", "NEW ZEALAND"],
    "AE": ["AE", "UAE", "阿联酋", "迪拜"],
    "TR": ["TR", "土耳其", "TURKEY"]
}

all_cleaned_lines = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for url in URLS:
    try:
        print(f"正在抓取: {url}")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode("utf-8")
            lines = content.splitlines()
            count = 0
            
            for line in lines:
                if not line.strip() or line.startswith('#'):
                    continue
                
                # 1. 彻底清除所有零宽空格和不可见控制字符
                for zc in ['\u200b', '\u200c', '\u200d', '\ufeff', '\u2003', '\u2002']:
                    line = line.replace(zc, '')
                
                # 2. 按 # 分割为 IP:端口 和 后面部分
                if '#' not in line:
                    continue
                parts = line.split('#', 1)
                ip_port = parts[0].strip()
                tail = parts[1].strip()
                
                # 3. 提取干净的基础名称
                if '|' in tail:
                    base_name = tail.split('|')[0].strip()
                else:
                    base_name = tail.strip()
                
                if not base_name:
                    base_name = "Mia优选"
                
                # 4. 智能匹配国家/地区代码
                detected_region = "OTH"
                upper_tail = tail.upper()
                
                matched = False
                for code, keywords in REGION_KEYWORDS.items():
                    for kw in keywords:
                        if kw in upper_tail:
                            detected_region = code
                            matched = True
                            break
                    if matched:
                        break
                
                # 5. 单字母切碎情况的特殊兜底映射
                if detected_region == "OTH":
                    if " |H|" in tail or " H " in tail: detected_region = "HK"
                    elif " |J|" in tail or " J " in tail: detected_region = "JP"
                    elif " |U|" in tail or " U " in tail: detected_region = "US"
                    elif " |S|" in tail or " S " in tail: detected_region = "SG"
                    elif " |T|" in tail or " T " in tail: detected_region = "TW"
                    elif " |K|" in tail or " K " in tail: detected_region = "KR"

                # 6. 组装成标准格式: IP:Port#名称 |地区|
                cleaned_line = f"{ip_port}#{base_name} |{detected_region}|"
                all_cleaned_lines.append(cleaned_line)
                count += 1
                
            print(f"成功处理 {url}，提取有效节点: {count} 个")
    except Exception as e:
        print(f"⚠️ 抓取或处理 {url} 失败（已跳过此网址）: {e}")

# 保存最终合并结果
with open("ipv4_cleaned.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_cleaned_lines))

print(f"所有订阅源处理完毕！总计合并节点: {len(all_cleaned_lines)} 个")
