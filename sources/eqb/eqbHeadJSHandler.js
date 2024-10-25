const CryptoJS = require('crypto-js');

bodyRaw = '{"docs":[{"fileId":"bb4e384768284e5fb5066106e11f7b9c","fileName":"TCL光伏科技“沐光同行 家国共贺”活动授权书.pdf"}],"flowInfo":{"autoArchive":true,"autoInitiate":true,"businessScene":"TCL光伏科技“沐光同行 家国共贺”活动授权书","flowConfigInfo":{"noticeDeveloperUrl":"https://callback1-pv.tcl.com/api/app/contract/unify/signed/callback/eqb","noticeType":"","redirectUrl":"","signPlatform":"1","willTypes":["FACE_TECENT_CLOUD_H5"]}},"signers":[{"platformSign":false,"signOrder":1,"signerAccount":{"signerAccountId":"84e5ece9f39d436c813b4dc2c521ad04"},"signfields":[{"autoExecute":false,"fileId":"bb4e384768284e5fb5066106e11f7b9c","sealType":"0","signDateBean":{"posPage":1,"posX":410.04,"posY":266.437},"posBean":{"posPage":"1","posX":458.0,"posY":316.477},"signDateBeanType":2}]}]}'
contentMd5 = CryptoJS.enc.Base64.stringify(CryptoJS.MD5(bodyRaw));

console.log(CryptoJS.MD5(bodyRaw).toString()) // 24db04a13392345380079902b6b9659c
console.log(contentMd5)                       // JNsEoTOSNFOAB5kCtrllnA==