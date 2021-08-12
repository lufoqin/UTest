export function table2jsonStr(content) {
  let res = '{'
  // console.log(content);
  for (let i = 0; i < content.length; i++) {
    let name = content[i]['name'].replaceAll('"', "'")
    // console.log(name);
    let value = content[i]['value'].replaceAll('"', "'")
    if (!name) {
      continue
    } else {
      res += '"' + name + '":' + '"' + value + '",'
    }
  }
  if (res === '{') {
    res = ""
  } else {
    res = res.slice(0, -1) + '}'
  }
  return res
}

export function str2jsonFormat(content) {
  let s = content
  let itemList
  let result = '{'
  if (s.substr(0, 1) === '{' && s.substr(s.length-1, 1) === '}') {
    s = s.slice(1, -1)
    console.log(s);
  }

  if (/\S+:.+,/.exec(s)) { // 如果匹配到类似 "TenantId": "{TenantId}", 的格式，则采用这种方式，
                          // 先替换换行符，然后以,进行切割
    console.log('111111');
    s = s.replaceAll('\n', ' ')
    itemList = s.split(',')
  } else { // 否则以 浏览器中form表单的形式进行处理，即格式中无,号，使用以\n进行切割
    console.log('22222');
    itemList = s.split('\n')
  }

  let reg = /(\S+):\s*(.+)/
  for (let i=0; i<itemList.length; i++) {
    let res = reg.exec(itemList[i])
    if (res) {
      if (res[1].substr(0, 1) === "'" || res[1].substr(0, 1) === '"'){
        result = result + res[1] +":"
      } else {
        result = result + '"' + res[1] + '"' + ':'
      }
      if (res[2].substr(0, 1) === "'" || res[2].substr(0, 1) === '"') {
        result =  result + res[2] + ","
      } else {
        result = result + '"' + res[2] + '"' + ','
      }
    }
  }
  result = result.slice(0, result.length-1)
  result = result + '}'
  if (result === '}') {
    result = ""
  }
  return result
}

export function preReset(obj, func, title, cancelMsg="已取消清空操作") {
  return obj.$confirm(title,"提示", {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
      func()
    }).catch(error => {
    console.log('=====');
    console.log(error);
      obj.$message({
      type: 'info',
      message: cancelMsg
  })
})
}

export function arrayCopy(arr) {
  let newArray = []
  for (let i=0; i<arr.length; i++) {
    newArray.push(arr[i])
  }
  return newArray
}
