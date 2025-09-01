import pandas as pd
import requests


PREFECTURE_STR2CODE_DICT = {
    "北海道": "01",
    "青森県": "02",
    "岩手県": "03",
    "宮城県": "04",
    "秋田県": "05",
    "山形県": "06",
    "福島県": "07",
    "茨城県": "08",
    "栃木県": "09",
    "群馬県": "10",
    "埼玉県": "11",
    "千葉県": "12",
    "東京都": "13",
    "神奈川県": "14",
    "新潟県": "15",
    "富山県": "16",
    "石川県": "17",
    "福井県": "18",
    "山梨県": "19",
    "長野県": "20",
    "岐阜県": "21",
    "静岡県": "22",
    "愛知県": "23",
    "三重県": "24",
    "滋賀県": "25",
    "京都府": "26",
    "大阪府": "27",
    "兵庫県": "28",
    "奈良県": "29",
    "和歌山県": "30",
    "鳥取県": "31",
    "島根県": "32",
    "岡山県": "33",
    "広島県": "34",
    "山口県": "35",
    "徳島県": "36",
    "香川県": "37",
    "愛媛県": "38",
    "高知県": "39",
    "福岡県": "40",
    "佐賀県": "41",
    "長崎県": "42",
    "熊本県": "43",
    "大分県": "44",
    "宮崎県": "45",
    "鹿児島県": "46",
    "沖縄県": "47"
}


def get_city_state_code(api_key, pref_id, want_to_know_code):
    api_url = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT002"
    header_api_dict = {"Ocp-Apim-Subscription-Key": api_key}
    param_api_dict = {"area": pref_id,
                      "language": "ja"}
    response = requests.request(method="GET",
                                url=api_url,
                                params=param_api_dict,
                                headers=header_api_dict)
    response_dict = response.json()
    city_state_id2name_dict_list = response_dict["data"]
    city_state_code = ""
    for city_state_id2name_dict in city_state_id2name_dict_list:
        if city_state_id2name_dict["name"] == want_to_know_code:
            city_state_code = city_state_id2name_dict["id"]
            break
        else:
            continue
    if not city_state_code:
        print("市区町村コード無し")
    return city_state_code


def get_price_data(api_key, prefecture_name, city_state_name, yyyy="2024"):
    prefecture_id = PREFECTURE_STR2CODE_DICT[prefecture_name]
    city_state_id = get_city_state_code(api_key=api_key,
                                        pref_id=prefecture_id,
                                        want_to_know_code=city_state_name)
    api_url = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
    header_api_dict = {"Ocp-Apim-Subscription-Key": api_key}
    param_api_dict = {"priceClassification": "01",
                      "year": yyyy,
                      "area": prefecture_id,
                      "city": city_state_id,
                      "language": "ja"}
    response = requests.request(method="GET",
                                url=api_url,
                                params=param_api_dict,
                                headers=header_api_dict)
    response_dict = response.json()
    df = pd.DataFrame(data=response_dict["data"])
    pickup_column = ["Region",
                     "Prefecture",
                     "Municipality",
                     "DistrictName",
                     "TradePrice",
                     "Area"]
    pickup_df = df[pickup_column].copy()
    pickup_2_df = pickup_df.query(expr="Region == '住宅地'").copy()
    pickup_2_df["result_PricePerArea"] = pickup_2_df["TradePrice"].astype(dtype=int) // pickup_2_df["Area"].astype(dtype=int)
    median_price_per_area = pickup_2_df["result_PricePerArea"].median()
    return pickup_2_df, median_price_per_area