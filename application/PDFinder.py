import aiohttp, asyncio
from flask import jsonify

async def pdFINDER(pertanyaan, count):
    async with aiohttp.ClientSession() as session:
        params = {
            "count": f"{count}",
            "find": f"{pertanyaan}",
        }
        async with session.get("https://openapi-idk8.onrender.com/pdf", params=params) as response:
            json_response = await response.json()
            if '\'results\':[]' not in str(json_response):
                PDF = []
                for data in json_response['results']:
                    title, url, snippet = data['title'], data['url'], data['snippet']
                    PDF.append({
                        "snippet": f"{snippet}",
                        "url": f"{url}",
                        "title": f"{title}"
                    })
                return jsonify({
                    "Sukses": True, "Message": PDF
                }), 200
            else:
                return jsonify({
                    "Sukses": False, "Message": "Tidak ada PDF yang ditemukan!"
                }), 200