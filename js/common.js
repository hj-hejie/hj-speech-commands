(function () {

    "use strict";

    $.extend($, {
    	
    	mask : function(){
        	$(".preloader", window.top==window?undefined:window.top.document).fadeIn();
    	},
    	
    	unmask : function(){
    		$(".preloader", window.top==window?undefined:window.top.document).fadeOut();
    	},
    	
    	mypost : function(url, func, param){
    		$.mask();
            $.ajax({
                url: url,
                method: 'POST',
                dataType : 'json',
                contentType : 'application/json',
                data: JSON.stringify(param == undefined ? {} : param),
                success: function(re){
                    if(re.success){
                    	func(re.value);
                    	$.unmask();
                    }else{
                    	debugger;
                    }
                },
                error: function(err){
                    debugger;
                }
            });
        },
        
        api: function(url, func, param){
        	$.mypost('../../api/'+url, func, param);
        },
        
        userinfo : function(func){
        	$.mypost('/userinfo', function(re){
        		
            	if(re == 402){
            		window.location.href='/app/views/login.html';
            	}
            	
            	$('.username').html(re.name);
            	
        		$('#welcome').html(re.name + '，欢迎您！');
        		
        	    $("#logout").click(function(){
        	    	$.mypost('/logout', function(re){
        	        	window.location.href='/app/views/login.html';
        	        });
        	    });
        		if(func){
        			func(re);
        		}
            });
        },
        
        fxbgjbxx : function(func){
        	$.api('fxbgjbxx', function(re){
        		var now = new Date();
        		re.nd=now.getFullYear();
        		re.jd=Math.ceil((now.getMonth()+1)/3)-1;
        		re.jdzw = re.jd == 1 ? '一' : re.jd == 2 ?  '二' : re.jd == 3 ? '三' : '四';
        		re.ndjd = re.nd + '年第' + re.jdzw + '季度';
        		$('.nd').html(re.nd);
        		$('.jdzw').html(re.jdzw);
        		$('.bjd').html(re.ndjd);
        		func(re);
        	});
        },
        
        assemble: function(element, data){
        	if(element.is('input')){
        		element.val(data);
        	}else{
        		element.empty();
        		element.append(data);
        	}
        },
        
        render : function(tmpId, data, prefix, filter){
        	if(!prefix) prefix = '.';
        	if(data instanceof Array){
        		var parent = $(tmpId);
        		var child = parent.children();
        		child.remove();
        		for(var i=0; i<data.length; i++){
            		var clone = child.clone();
            		if(data[i] instanceof Object){
            			for(var j in data[i]){
            				var jqEle = clone.find(prefix + j);
            				if(jqEle.length > 0){
            					var content = data[i][j];
            					if(filter){
            						var filtcontent = filter(j, content);
            						content = filtcontent ? filtcontent: content;
            					}
            					$.assemble(jqEle, content);
            				}
            			}
            			var thisEle = clone.find(prefix + 'this');
        				if(thisEle.length > 0){
        					var content = data[i];
        					if(filter){
        						var filtcontent = filter("this", content);
        						content = filtcontent ? filtcontent: content;
        					}
        					$.assemble(thisEle, content);
        				}
            			
        				var xhEle = clone.find(prefix + 'xh');
        				if(xhEle.length > 0){
        					xhEle.html(i+1);
        				}
            		}else{
            			var content = data[i];
    					if(filter){
    						var filtcontent = filter(j, content);
    						content = filtcontent ? filtcontent: content;
    					}
    					$.assemble(clone, content);
            		}
    				
        			clone.appendTo(parent);
        		}
        	}else{
		    	for(var i in data){
		    		var jqEle = $(tmpId + ' ' + prefix + i);
		    		if(jqEle.length > 0){
		    			var content = data[i];
		    			if(filter){
    						var filtcontent = filter(i, content);
    						content = filtcontent ? filtcontent: content;
    					}
		    			$.assemble(jqEle, content);
		    		}
		    	}
        	}
        },
        
        unrender : function(data, tmpId, prefix, filter){
        	if(!prefix) prefix = '.';
        	for(var i in data){
	    		var jqEle = $(tmpId + ' ' + prefix + i);
	    		if(jqEle.length > 0){
	            	if(jqEle.is('input')){
	            		data[i]=jqEle.val();
	            	}else{
	            		data[i]=jqEle.html();
	            	}
	    		}
	    	}
        }
    });

})();