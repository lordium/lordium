(function(window,angular,undefined){'use strict';var isArray=angular.isArray;var forEach=angular.forEach;var isString=angular.isString;var jqLite=angular.element;angular.module('ngMessages',[]).directive('ngMessages',['$animate',function($animate){var ACTIVE_CLASS='ng-active';var INACTIVE_CLASS='ng-inactive';return{require:'ngMessages',restrict:'AE',controller:['$element','$scope','$attrs',function($element,$scope,$attrs){var ctrl=this;var latestKey=0;var nextAttachId=0;this.getAttachId=function getAttachId(){return nextAttachId++;};var messages=this.messages={};var renderLater,cachedCollection;this.render=function(collection){collection=collection||{};renderLater=false;cachedCollection=collection;var multiple=isAttrTruthy($scope,$attrs.ngMessagesMultiple)||isAttrTruthy($scope,$attrs.multiple);var unmatchedMessages=[];var matchedKeys={};var messageItem=ctrl.head;var messageFound=false;var totalMessages=0;while(messageItem!=null){totalMessages++;var messageCtrl=messageItem.message;var messageUsed=false;if(!messageFound){forEach(collection,function(value,key){if(!messageUsed&&truthy(value)&&messageCtrl.test(key)){if(matchedKeys[key])return;matchedKeys[key]=true;messageUsed=true;messageCtrl.attach();}});}
if(messageUsed){messageFound=!multiple;}else{unmatchedMessages.push(messageCtrl);}
messageItem=messageItem.next;}
forEach(unmatchedMessages,function(messageCtrl){messageCtrl.detach();});unmatchedMessages.length!==totalMessages?$animate.setClass($element,ACTIVE_CLASS,INACTIVE_CLASS):$animate.setClass($element,INACTIVE_CLASS,ACTIVE_CLASS);};$scope.$watchCollection($attrs.ngMessages||$attrs['for'],ctrl.render);this.reRender=function(){if(!renderLater){renderLater=true;$scope.$evalAsync(function(){if(renderLater){cachedCollection&&ctrl.render(cachedCollection);}});}};this.register=function(comment,messageCtrl){var nextKey=latestKey.toString();messages[nextKey]={message:messageCtrl};insertMessageNode($element[0],comment,nextKey);comment.$$ngMessageNode=nextKey;latestKey++;ctrl.reRender();};this.deregister=function(comment){var key=comment.$$ngMessageNode;delete comment.$$ngMessageNode;removeMessageNode($element[0],comment,key);delete messages[key];ctrl.reRender();};function findPreviousMessage(parent,comment){var prevNode=comment;var parentLookup=[];while(prevNode&&prevNode!==parent){var prevKey=prevNode.$$ngMessageNode;if(prevKey&&prevKey.length){return messages[prevKey];}
if(prevNode.childNodes.length&&parentLookup.indexOf(prevNode)==-1){parentLookup.push(prevNode);prevNode=prevNode.childNodes[prevNode.childNodes.length-1];}else{prevNode=prevNode.previousSibling||prevNode.parentNode;}}}
function insertMessageNode(parent,comment,key){var messageNode=messages[key];if(!ctrl.head){ctrl.head=messageNode;}else{var match=findPreviousMessage(parent,comment);if(match){messageNode.next=match.next;match.next=messageNode;}else{messageNode.next=ctrl.head;ctrl.head=messageNode;}}}
function removeMessageNode(parent,comment,key){var messageNode=messages[key];var match=findPreviousMessage(parent,comment);if(match){match.next=messageNode.next;}else{ctrl.head=messageNode.next;}}}]};function isAttrTruthy(scope,attr){return(isString(attr)&&attr.length===0)||truthy(scope.$eval(attr));}
function truthy(val){return isString(val)?val.length:!!val;}}]).directive('ngMessagesInclude',['$templateRequest','$document','$compile',function($templateRequest,$document,$compile){return{restrict:'AE',require:'^^ngMessages',link:function($scope,element,attrs){var src=attrs.ngMessagesInclude||attrs.src;$templateRequest(src).then(function(html){$compile(html)($scope,function(contents){element.after(contents);var anchor=jqLite($document[0].createComment(' ngMessagesInclude: '+src+' '));element.after(anchor);element.remove();});});}};}]).directive('ngMessage',ngMessageDirectiveFactory('AE')).directive('ngMessageExp',ngMessageDirectiveFactory('A'));function ngMessageDirectiveFactory(restrict){return['$animate',function($animate){return{restrict:'AE',transclude:'element',terminal:true,require:'^^ngMessages',link:function(scope,element,attrs,ngMessagesCtrl,$transclude){var commentNode=element[0];var records;var staticExp=attrs.ngMessage||attrs.when;var dynamicExp=attrs.ngMessageExp||attrs.whenExp;var assignRecords=function(items){records=items?(isArray(items)?items:items.split(/[\s,]+/)):null;ngMessagesCtrl.reRender();};if(dynamicExp){assignRecords(scope.$eval(dynamicExp));scope.$watchCollection(dynamicExp,assignRecords);}else{assignRecords(staticExp);}
var currentElement,messageCtrl;ngMessagesCtrl.register(commentNode,messageCtrl={test:function(name){return contains(records,name);},attach:function(){if(!currentElement){$transclude(scope,function(elm){$animate.enter(elm,null,element);currentElement=elm;var $$attachId=currentElement.$$attachId=ngMessagesCtrl.getAttachId();currentElement.on('$destroy',function(){if(currentElement&&currentElement.$$attachId===$$attachId){ngMessagesCtrl.deregister(commentNode);messageCtrl.detach();}});});}},detach:function(){if(currentElement){var elm=currentElement;currentElement=null;$animate.leave(elm);}}});}};}];function contains(collection,key){if(collection){return isArray(collection)?collection.indexOf(key)>=0:collection.hasOwnProperty(key);}}}})(window,window.angular);