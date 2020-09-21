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

## cancel

- 交易撤销

- api:/trade/tcancel,POST

- options可选，传递内容详见Python API手册P39

- content：

- ```json
  
  {
      "OrderNumber":"",
      "options":{
          "OrderNumber":"",
          "MarketType":"",
          "LogonID":""
    
      }
  }
  ```

- 

## query

- 查询交易

- api:/trade/tquery,POST

- options可选，详细内容在Python手册P42

- contet：

  ```json
  {
      "queryType":"",
      "options":{
          "LogonID":"",
          "RequestID":"",
          "OrderNumber":"",
          "MarketType":"",
          "OrderType":"",
          "WindCode":"",
    
      }
  }
  ```

  