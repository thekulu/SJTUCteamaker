let btnAll = document.getElementByTagName('button')
let conAll = document.getElementByClassName('content')
let btnAllLen = btnAll.length

//为每个按钮的click事件创建一个回调函数
for(let i=0;i<btnAllLen;i++){
    !(function(n){								// 注册click事件
        btnAll[n].addEventListener('click',function(){
            for(let j=0;j<btnAlllen;j++){		
                btn[j].className = ""			
                conAll[j].style.display = "none"	
            }
            this.className ="active"
            conAll[n].style.display = "block"
        })
    })(i)
}