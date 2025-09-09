(async () => {
  // 获取 token
  const fb_dtsg = require("DTSGInitData").token;
  const lsd = require("LSD").token;

  // 你的参数
  const variables = {
    businessID: "2011663792630181",
    assetIDs: [
      "120204419101590324",
      "120203582798190774",
      "120203486144090213",
      "120203644201460700",
      "120204857630550563",
      "120204140401320354",
      "120203530519870769",
      "120204377443630676",
      "120203717139360103",
      "120203775244880578",
      "120207524384160059",
      "120204280525560418",
      "120203532700660762",
      "120203662571780666",
      "120204183676210443",
      "120204926889790360",
      "120204394462200291",
      "120205712952390729",
      "120204239873910568",
      "120205541929400409"
    ],
    userID: "61579876804061",
    taskIDs: [
      "864195700451909",
      "151821535410699",
      "610690166001223",
      "186595505260379"
    ],
    assetTypes: [
      "PAGE", "AD_ACCOUNT", "PRODUCT_CATALOG", "APP", "PIXEL",
      "INSTAGRAM_ACCOUNT_V2", "OFFLINE_CONVERSION_DATA_SET",
      "BLOCK_LIST", "OWNED_DOMAIN", "WHATSAPP_BUSINESS_ACCOUNT",
      "BUSINESS_RESOURCE_GROUP", "BUSINESS_CREATIVE_FOLDER",
      "EVENTS_DATASET_NEW"
    ],
    countLimit: 51,
    shouldRecommendAssets: false
  };

  // 发请求
  const res = await fetch("https://business.facebook.com/api/graphql/", {
    method: "POST",
    headers: {
      "content-type": "application/x-www-form-urlencoded",
      "x-fb-friendly-name": "useBulkAssignAssetsToUsersMutation"
    },
    body: new URLSearchParams({
      fb_dtsg,
      lsd,
      variables: JSON.stringify(variables),
      doc_id: "24538812169083010"
    }),
    credentials: "include"
  });

  const data = await res.json();
  console.log("返回结果:", data);
})();
