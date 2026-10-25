import re
import urllib.request

# 1. 在这里配置你的所有订阅网址（想加第二个、第三个直接往列表里加逗号隔开即可）
URLS = [
    "https://bestcf.pages.dev/xinyitang3/ipv4.txt",
    # "https://raw.githubusercontent.com/LancelotRar/best-cf-ips/refs/heads/main/best-cf-ip-collected.txt",
    # "https://bestcf.pages.dev/cfyes/ipv4.txt",
    # "https://bestcf.pages.dev/s5gy/jp.txt",
    # "https://bestcf.pages.dev/s5gy/tw.txt",
    # "https://bestcf.pages.dev/tiancheng2/tw.txt",
    # "https://bestcf.pages.dev/uouin/all.txt",
    # ""
]
# 常见国家/地区代码映射表
REGION_MAP = {
    "HK": "HK", "HONGKONG": "HK", "香港": "HK",
    "TW": "TW", "TAIWAN": "TW", "台湾": "TW", "台灣": "TW",
    "MO": "MO", "MACAU": "MO", "澳门": "MO",
    "JP": "JP", "JAPAN": "JP", "日本": "JP", "东京": "JP", "大阪": "JP",
    "KR": "KR", "KOREA": "KR", "韩国": "KR", "首尔": "KR",
    "SG": "SG", "SINGAPORE": "SG", "新加坡": "SG",
    "MY": "MY", "MALAYSIA": "MY", "马来西亚": "MY",
    "TH": "TH", "THAILAND": "TH", "泰国": "TH",
    "VN": "VN", "VIETNAM": "VN", "越南": "VN",
    "PH": "PH", "PHILIPPINES": "PH", "菲律宾": "PH",
    "US": "US", "USA": "US", "UNITEDSTATES": "US", "美国": "US", "美": "US",
    "CA": "CA", "CANADA": "CA", "加拿大": "CA",
    "BR": "BR", "BRAZIL": "BR", "巴西": "BR",
    "GB": "GB", "UK": "GB", "UNITEDKINGDOM": "GB", "英国": "GB", "英": "GB",
    "DE": "DE", "GERMANY": "DE", "德国": "DE",
    "FR": "FR", "FRANCE": "FR", "法国": "FR",
    "NL": "NL", "NETHERLANDS": "NL", "荷兰": "NL",
    "CH": "CH", "SWITZERLAND": "CH", "瑞士": "CH",
    "IT": "IT", "ITALY": "IT", "意大利": "IT",
    "ES": "ES", "SPAIN": "ES", "西班牙": "ES",
    "SE": "SE", "SWEDEN": "SE", "瑞典": "SE",
    "IE": "IE", "IRELAND": "IE", "爱尔兰": "IE",
    "NO": "NO", "NORWAY": "NO", "挪威": "NO",
    "FI": "FI", "FINLAND": "FI", "芬兰": "FI",
    "AU": "AU", "AUSTRALIA": "AU", "澳大利亚": "AU", "澳洲": "AU",
    "NZ": "NZ", "NEWZEALAND": "NZ", "新西兰": "NZ",
    "AE": "AE", "UAE": "AE", "阿联酋": "AE", "迪拜": "AE",
    "TR": "TR", "TURKEY": "TR", "土耳其": "TR"
}

all_cleaned_lines = []

# 模拟主流浏览器请求头，降低被 403 拦截的概率
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
                    
                # 匹配形如 IP:端口#名称 | 地区 | 或其他变体的结构
                match = re.search(r'^([^#]+)#([^|]+)\|\s*(.+?)(?:\s*\||$)', line)
                if match:
                    ip_port = match.group(1).strip()
                    name = match.group(2).strip()
                    raw_region = match.group(3).strip()
                    
                    cleaned_region_str = "".join(raw_region.split()).upper()
                    standard_region = REGION_MAP.get(cleaned_region_str, None)
                    
                    if not standard_region and len(cleaned_region_str) >= 2:
                        potential_code = cleaned_region_str[:2]
                        if potential_code in REGION_MAP.values():
                            standard_region = potential_code
                        else:
                            standard_region = cleaned_region_str[:2]
                    
                    if not standard_region:
                        standard_region = "OTH"
                        
                    cleaned_line = f"{ip_port}#{name} |{standard_region}|"
                    all_cleaned_lines.append(cleaned_line)
                    count += 1
            print(f"成功处理 {url}，提取有效节点: {count} 个")
            
    except Exception as e:
        print(f" 抓取或处理 {url} 失败（已跳过此网址）: {e}")

# 保存最终合并结果
with open("ipv4_cleaned.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_cleaned_lines))

print(f"所有订阅源处理完毕！总计合并节点: {len(all_cleaned_lines)} 个")
