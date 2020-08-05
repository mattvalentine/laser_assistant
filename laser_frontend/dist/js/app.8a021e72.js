(function(e){function t(t){for(var a,i,o=t[0],u=t[1],l=t[2],p=0,d=[];p<o.length;p++)i=o[p],Object.prototype.hasOwnProperty.call(r,i)&&r[i]&&d.push(r[i][0]),r[i]=0;for(a in u)Object.prototype.hasOwnProperty.call(u,a)&&(e[a]=u[a]);c&&c(t);while(d.length)d.shift()();return s.push.apply(s,l||[]),n()}function n(){for(var e,t=0;t<s.length;t++){for(var n=s[t],a=!0,o=1;o<n.length;o++){var u=n[o];0!==r[u]&&(a=!1)}a&&(s.splice(t--,1),e=i(i.s=n[0]))}return e}var a={},r={app:0},s=[];function i(t){if(a[t])return a[t].exports;var n=a[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,i),n.l=!0,n.exports}i.m=e,i.c=a,i.d=function(e,t,n){i.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},i.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.t=function(e,t){if(1&t&&(e=i(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(i.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)i.d(n,a,function(t){return e[t]}.bind(null,a));return n},i.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return i.d(t,"a",t),t},i.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},i.p="/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],u=o.push.bind(o);o.push=t,o=o.slice();for(var l=0;l<o.length;l++)t(o[l]);var c=u;s.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"01ef":function(e,t,n){},"034f":function(e,t,n){"use strict";var a=n("85ec"),r=n.n(a);r.a},"1ac7":function(e,t,n){"use strict";var a=n("672b"),r=n.n(a);r.a},"2f46":function(e,t,n){},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var a=n("2b0e"),r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"ui",attrs:{id:"app"}},[e.svgLoaded?n("OutputSVG",{attrs:{outsvg:e.outputModel}}):e._e(),e.svgLoaded?n("EdgeSVG",{attrs:{edge_data:e.inputModel.edge_data},on:{addJoint:e.addJoint}}):e._e(),e.svgLoaded?n("Parameters",{attrs:{thickness:e.laserParams.thickness,kerf:e.laserParams.kerf},on:{update:e.updateParams}}):e._e(),e.svgLoaded?e._e():n("LoadSVG",{on:{insvg:e.loadSVG}})],1)},s=[],i=(n("d3b7"),n("25f0"),function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"output model",domProps:{innerHTML:e._s(e.outsvg)}})}),o=[],u={name:"OutputSVG",props:["outsvg"]},l=u,c=(n("d750"),n("2877")),p=Object(c["a"])(l,i,o,!1,null,null,null),d=p.exports,f=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"edge-layer model"},[n("svg",{attrs:{id:"Layer",viewBox:e.edge_data.viewBox,xmlns:"http://www.w3.org/2000/svg"}},[n("g",{attrs:{id:"clickedges"}},e._l(e.edge_data.edges,(function(t){return n("path",{key:t.edge,staticClass:"edges",attrs:{d:t.d},on:{click:function(n){return e.edgeClicked(t)}}})})),0)])])},m=[],v={name:"EdgeSVG",props:["edge_data"],data:function(){return{output_svg:""}},methods:{edgeClicked:function(e){console.log(e),this.$emit("addJoint",e)}}},h=v,g=(n("7bcc"),Object(c["a"])(h,f,m,!1,null,null,null)),_=g.exports,b=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"params"},[n("p",[e._v(" Thickness (mm): "),n("br"),n("input",{directives:[{name:"model",rawName:"v-model",value:e.newThickness,expression:"newThickness"}],attrs:{name:"thickness",type:"number",step:"0.1"},domProps:{value:e.newThickness},on:{change:e.applyParams,input:function(t){t.target.composing||(e.newThickness=t.target.value)}}})]),n("p",[e._v(" Material "),n("br"),n("select",{directives:[{name:"model",rawName:"v-model",value:e.material,expression:"material"}],attrs:{name:"material"},on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){var t="_value"in e?e._value:e.value;return t}));e.material=t.target.multiple?n:n[0]}}},[n("option",{attrs:{disabled:"",value:""}},[e._v("Please select one")]),n("option",[e._v("Wood")]),n("option",[e._v("Acrylic")])])]),n("p",[e._v(" Kerf Radius (mm): "),n("br"),n("input",{directives:[{name:"model",rawName:"v-model",value:e.newKerf,expression:"newKerf"}],attrs:{name:"kerf",type:"number",step:"0.01"},domProps:{value:e.newKerf},on:{change:e.applyParams,input:function(t){t.target.composing||(e.newKerf=t.target.value)}}})]),n("button",{on:{click:e.applyParams}},[e._v("Apply")])])},w=[],y={name:"Parameters",props:["thickness","kerf"],data:function(){return{newThickness:3.1,newKerf:.27,material:"Acrylic"}},mounted:function(){this.newThickness=this.thickness,this.newKerf=this.kerf},methods:{applyParams:function(){var e=parseFloat(this.newThickness),t=parseFloat(this.newKerf);this.$emit("update",{thickness:e,kerf:t})}}},k=y,O=(n("9d43"),Object(c["a"])(k,b,w,!1,null,"730ce79a",null)),P=O.exports,x=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"loader"},[n("span",[n("input",{staticClass:"loadbutton",attrs:{type:"file",id:"SVGfile"},on:{change:e.printFile}})])])},S=[],j=(n("96cf"),n("1da1")),M={name:"LoadSVG",methods:{printFile:function(){var e=Object(j["a"])(regeneratorRuntime.mark((function e(t){var n,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n=t.target.files[0],e.next=3,new Response(n).text();case 3:return a=e.sent,console.log(a),this.$emit("insvg",a),e.abrupt("return");case 7:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}()}},T=M,G=(n("1ac7"),Object(c["a"])(T,x,S,!1,null,null,null)),V=G.exports,A=n("bc3a").default,C={name:"App",components:{OutputSVG:d,EdgeSVG:_,Parameters:P,LoadSVG:V},data:function(){return{svgLoaded:!1,outputModel:"<svg/>",inputModel:{},laserParams:{thickness:3.1,kerf:.27},AB:!0,joint_index:1}},methods:{loadSVG:function(e){var t=this;this.svgLoaded=!0;var n=new FormData;n.append("svgInput",e),A.post("get_model",n,{headers:{"Content-Type":"multipart/form-data"}}).then((function(e){t.inputModel=e.data,t.updateOutput()}))},updateOutput:function(){var e=this,t=new FormData;t.append("inputModel",JSON.stringify(this.inputModel)),t.append("laserParams",JSON.stringify(this.laserParams)),A.post("get_output",t,{headers:{"Content-Type":"multipart/form-data"}}).then((function(t){e.outputModel=t.data}))},updateParams:function(e){console.log(e),this.laserParams=e,this.updateOutput()},addJoint:function(e){var t="J"+this.joint_index.toString()+(this.AB?"A":"B");this.inputModel.joints[t]={path:e.d,face:e.face},this.AB=!this.AB,!0===this.AB&&(this.joint_index+=1),this.updateOutput()}}},L=C,J=(n("034f"),Object(c["a"])(L,r,s,!1,null,null,null)),$=J.exports;a["a"].config.productionTip=!1,new a["a"]({render:function(e){return e($)}}).$mount("#app")},"672b":function(e,t,n){},"6e00":function(e,t,n){},"7bcc":function(e,t,n){"use strict";var a=n("01ef"),r=n.n(a);r.a},"85ec":function(e,t,n){},"9d43":function(e,t,n){"use strict";var a=n("6e00"),r=n.n(a);r.a},d750:function(e,t,n){"use strict";var a=n("2f46"),r=n.n(a);r.a}});
//# sourceMappingURL=app.8a021e72.js.map