## logon
- api: /trade/tlogon, POST
- accountType可选
- content:
  ```json
  {
  	"brokerId": "",
  	"departmentId": "",
  	"logonAccount": "",
  	"password": "",
  	"accountType": ""
  }
  ```


## logout
- api: /trade/tlogout, POST
- logonId可选，默认0
- content:
  ```json
  {
  	"logonId": ""
  }
  ```

## order
- 交易委托下单
- api: /trade/torder, POST
- options可选，传递内容详见Python API手册 Page.36
- content:
  ```json
  {
  	"securityCode": "",
  	"tradeSide": "",
  	"orderPrice": "",
  	"orderVolume": "",

  	"options": {
  		"OrderType": "LMT",
  		"HedgeType": "SPEC"
  	}
  }
  ```