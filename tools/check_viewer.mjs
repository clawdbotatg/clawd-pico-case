// Browser smoke test against a locally launched Chromium debug port.
// Generates screenshots; does not control the printer or change geometry.
import {writeFile} from 'node:fs/promises';
const page = await (await fetch('http://127.0.0.1:9333/json/new?about:blank', {method:'PUT'})).json();
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(resolve => ws.addEventListener('open', resolve, {once:true}));
let id=0;
const pending=new Map();
ws.addEventListener('message', event => {
  const value=JSON.parse(event.data);
  if(pending.has(value.id)) {pending.get(value.id)(value);pending.delete(value.id);}
});
async function call(method, params={}) {
  const next=++id;
  const reply=new Promise(resolve=>pending.set(next,resolve));
  ws.send(JSON.stringify({id:next,method,params}));
  const value=await reply;
  if(value.error)throw Error(JSON.stringify(value.error));
  return value.result;
}
async function evaluate(expression) {
  const result=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
  if(result.exceptionDetails) throw Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
await call('Page.enable');
await call('Emulation.setDeviceMetricsOverride',{width:1280,height:900,deviceScaleFactor:1,mobile:false});
await call('Page.addScriptToEvaluateOnNewDocument',{source:'window.viewerErrors=[];addEventListener("error",e=>viewerErrors.push(e.message));'});
await call('Page.navigate',{url:process.env.VIEWER_URL || 'http://127.0.0.1:8793/viewer.html'});
for(let attempt=0;attempt<30;attempt++) {
  if(await evaluate('!!document.querySelector("#p-lid")')) break;
  await new Promise(resolve=>setTimeout(resolve,500));
}
console.log(await evaluate('JSON.stringify({errors:viewerErrors,parts:Object.keys(meshes),triangles:renderer.info.render.triangles,title:document.title})'));
const expectedParts=Number(process.env.EXPECTED_PARTS || 7);
if(!await evaluate(`viewerErrors.length===0 && Object.keys(meshes).length===${expectedParts} && renderer.info.render.triangles>0`)) throw Error('Viewer failed to render');
let shot=await call('Page.captureScreenshot',{format:'png'});
await writeFile(process.env.SCREENSHOT_PATH || 'renders/v3-browser.png',Buffer.from(shot.data,'base64'));
await evaluate('document.querySelector("[data-v=usb]").click();document.querySelector("#explode").value=12;document.querySelector("#explode").dispatchEvent(new Event("input"));document.querySelector("#opacity").value=.4;document.querySelector("#opacity").dispatchEvent(new Event("input"));');
if(!await evaluate('meshes.lid.position.z>0 && meshes.lid.material.opacity===.4'))throw Error('Viewer controls failed');
await evaluate('document.querySelector("#p-lid").click()');
if(!await evaluate('meshes.lid.visible===false'))throw Error('Part toggle failed');
await evaluate('document.querySelector("#p-lid").click()');
const before=await evaluate('theta');
await call('Input.dispatchMouseEvent',{type:'mousePressed',x:400,y:300,button:'left',clickCount:1});
await call('Input.dispatchMouseEvent',{type:'mouseMoved',x:500,y:340,button:'left',buttons:1});
await call('Input.dispatchMouseEvent',{type:'mouseReleased',x:500,y:340,button:'left',clickCount:1});
if(await evaluate('theta')===before)throw Error('Drag did not rotate');
console.log('PASS: render, view button, explode, transparency, part toggle, drag orbit');
ws.close();
