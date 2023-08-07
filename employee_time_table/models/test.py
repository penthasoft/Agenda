import requests

url_theme_post = "https://db6022c5515c7971bd9dc01e79165677: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@familystoretest.myshopify.com/admin/api/2020-10/themes/114144739494/assets.json"
myobj = {
      "asset": {
        "key": "layout/theme.liquid",
        "value": "{{content_for_header}}<script>console.log('foo')</script>,{{content_for_layout}}<script>console.log('foo123')</script>"
      }
    }
res = requests.put(url_theme_post,data ={"key": "layout/theme.liquid","value": "{{content_for_header}}<script>console.log('foo')</script>,{{content_for_layout}}<script>console.log('foo123')</script>"})
print('res', res)