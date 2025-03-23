// kakaku.comで最低価格を取得するGASスクリプト

function getPriceComPrice() {
  // 対象URL
  const url = "https://kakaku.com/item/xxxxxxxxx/";

  try {
    // URLからHTMLを取得
    const response = UrlFetchApp.fetch(url);
    const html = response.getContentText('UTF-8');

    // HTMLをパース (正規表現で価格部分を抽出)
    const priceMatch = html.match(/<span id="minPrice">.*?<a.*?<span>(.*?)～?<\/span><\/a>/s);

    // const priceMatch = html.match(/<span>¥(.*?)～<\/span>/s);

    if (priceMatch && priceMatch[1]) {
      let priceText = priceMatch[1].trim().replace(/,/g, '');
      let price = parseInt(priceText.match(/\d+/s));

      // スプレッドシートに書き込み
      const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
      const sheet = spreadsheet.getSheetByName("シート1");
      const now = Utilities.formatDate(new Date(), "JST", "yyyy/MM/dd HH:mm:ss");

      sheet.appendRow([now, price]);

      Logger.log("価格を取得してスプレッドシートに書き込みました: " + price + "円");

    } else {
      Logger.log("最低価格情報をHTMLから抽出できませんでした。HTML構造が変更された可能性があります。");
      Logger.log("取得したHTML:\n" + html);
    }

  } catch (e) {
    Logger.log("エラーが発生しました: " + e);
  }
}

// メニューをスプレッドシートに追加 (手動実行用)
function onOpenSpreadsheet() {
  SpreadsheetApp.getUi()
      .createMenu('Price Tracker')
      .addItem('Get Price', 'getPriceComPrice')
      .addToUi();
}
