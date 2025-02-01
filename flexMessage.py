import requests

def get_exchange_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/JPY")
        data = response.json()
        if "rates" in data:
            return data["rates"]
        else:
            print("為替レート情報が取得できませんでした:", data)
            return {}
    except Exception as e:
        print("Exchange rate error:", e)
        return {}

def unitConvert(unit):
    if unit == "day":
        return "日"
    elif unit == "week":
        return "週"
    elif unit == "month":
        return "月"
    elif unit == "year":
        return "年"
    else:
        return "(不明)"

def item(item, day):
    # 料金のフォーマット処理
    if item["currency"] == "JPY":
        # JPYの場合は整数にして3桁ごとにカンマ区切りで表示
        price_text = "JPY " + format(int(item["price"]), ",")
    else:
        # 外貨の場合、APIから毎回為替レートを取得して換算する
        exchange_rates = get_exchange_rates()
        if item["currency"] in exchange_rates:
            rate = exchange_rates[item["currency"]]
            # 外貨価格から JPY 換算値を計算（例：USDの場合：price / rate）
            converted = float(item["price"]) / rate
            price_text = (f'{item["currency"]} ' +
                          format(float(item["price"]), ",.2f") +
                          f'（約 JPY {format(converted, ",.2f")}）')
        else:
            price_text = (f'{item["currency"]} ' +
                          format(float(item["price"]), ",.2f") +
                          "（レート取得エラー）")
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": day + "更新",
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "text",
            "text": item["name"],
            "weight": "bold",
            "size": "xl",
            "wrap": True,
            "margin": "md"
          },
          {
            "type": "text",
            "text": price_text,
            "weight": "regular",
            "size": "lg",
            "wrap": True,
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1,
                    "text": "更新日"
                  },
                  {
                    "type": "text",
                    "text": item["next_date"],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1,
                    "text": "頻度"
                  },
                  {
                    "type": "text",
                    "text": f'{item["interval"]}ヶ{unitConvert(item['unit'])}毎',
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "状況",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "停止中" if item["pause"] else "契約中",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 4
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "請求先",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": item["payment_method"],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 4
                  }
                ]
              }
            ]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "編集",
              "uri": "https://liff.line.me/2006629352-naO0NMkB/items/" + item["id"]
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "削除",
              "text": "> delete confirm " + item["id"]
            },
            "color": "#ED1A3D"
          }
        ],
        "flex": 0
      },
    }
    
    if "memo" in item:
        data["body"]["contents"][3]["contents"].append({
          "type": "box",
          "layout": "baseline",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "メモ",
              "color": "#aaaaaa",
              "size": "sm",
              "flex": 1
            },
            {
              "type": "text",
              "text": item["memo"],
              "wrap": True,
              "color": "#666666",
              "size": "sm",
              "flex": 4
            }
          ]
        })
    
    return data
