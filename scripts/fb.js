(()=>{
const H=675, KMAX=31, KMIN=12, KSPLIT=17;
const root=document.createElement('div');root.id='fbroot';document.body.appendChild(root);
const out=[];
function fits(p){return p.querySelector('.fbw').scrollHeight<=H}
function fit(p,lo,hi){ // largest k that fits
  p.style.setProperty('--k',lo+'px'); if(!fits(p)) return null;
  let a=lo,b=hi;
  while(b-a>0.25){const m=(a+b)/2;p.style.setProperty('--k',m+'px'); if(fits(p)) a=m; else b=m;}
  p.style.setProperty('--k',a+'px'); return a;
}
function mk(sec,part){
  const p=document.createElement('div');p.className='fbp';
  const w=document.createElement('div');w.className='fbw';
  const c=sec.cloneNode(true);c.removeAttribute('id');c.style.display='block';
  c.querySelectorAll('.fid').forEach(e=>{e.textContent=e.textContent.replace(/\s*·\s*صفحة\s*\d+\s*من\s*\d+/,'')});w.appendChild(c);p.appendChild(w);root.appendChild(p);p.dataset.id=sec.id;p.dataset.part=part;return p;
}
document.querySelectorAll('section.page').forEach(sec=>{
  const isCard=!!sec.querySelector('.card .rt');
  if(!isCard){out.push([sec.id,'W','-']);return;}
  const p=mk(sec,'0');
  let k=fit(p,KMIN,KMAX);
  if(k===null){p.style.setProperty('--k',KMIN+'px');const w=p.querySelector('.fbw');const sc=H/w.scrollHeight;w.style.transform=`scale(${sc})`;w.style.transformOrigin='top center';out.push([sec.id,'0','S'+sc.toFixed(2)]);return;}
  out.push([sec.id,'0',k.toFixed(1)]);
});
return out;
})()
