import json
src=open('scene.html').read()
js=src[src.index('<script>\nconst L'):]
R=[
('window.DURATION=L[N-1].end+2.2;','window.DURATION=L[N-1].end+2.6;'),
('c.fillRect(0,0,1080,1920)','c.fillRect(-700,0,2480,1920)'),
('c.fillRect(-200,-200,1480,2320)','c.fillRect(-800,-200,2680,2320)'),
('c.fillRect(rnd(i+3)*1080,rnd(i+7)*700,3,3)','c.fillRect(rnd(i+3)*2400-660,rnd(i+7)*700,3,3)'),
('for(let i=0;i<60;i++)','for(let i=0;i<130;i++)'),
('const B=[[0,1000,160],','const B=[[-660,950,180],[-470,880,150],[-300,1000,170],[-150,920,140],[1080,960,160],[1250,890,170],[1430,1000,140],[1580,930,180],[0,1000,160],'),
('for(let i=0;i<24;i++){const x=i*48;const y=y0+40*Math.sin(i/23*Math.PI)','for(let i=0;i<52;i++){const x=-700+i*48;const y=y0+40*Math.sin(i/51*Math.PI)'),
('c.fillRect(-200,1500,1480,700)','c.fillRect(-800,1500,2680,700)'),
('for(let i=0;i<7;i++)diya(80+i*155','for(let i=-4;i<11;i++)diya(80+i*155'),
('c.fillRect(0,300,1080,1100)','c.fillRect(-700,300,2480,1100)'),
('for(let i=0;i<9;i++)diya(70+i*120','for(let i=-6;i<15;i++)diya(70+i*120'),
('for(let i=0;i<24;i++){const x=i*48;const y=330+30*Math.sin(i/23*Math.PI)','for(let i=0;i<52;i++){const x=-700+i*48;const y=330+30*Math.sin(i/51*Math.PI)'),
('for(let i=0;i<3;i++)diya(240+i*300','for(let i=-2;i<6;i++)diya(240+i*300'),
('c.fillRect(rnd(i)*1080,(rnd(i+9)*1920','c.fillRect(rnd(i)*2400-660,(rnd(i+9)*1920'),
(' c.clearRect(0,0,1080,1920);',' c.setTransform(1,0,0,1,0,0);c.clearRect(0,0,1920,1080);c.translate(960,540);c.scale(.8,.8);c.translate(-540,-1005);'),
('else if(t<s(7)){chartBg()}','else {chartBg()}'),
('$("strike").style.width=(780*','$("strike").style.width=(700*'),
('$("bar0").style.height=(460*ease((t-b0+0.1)/0.6))+"px"; $("v0").style.opacity=clamp((t-b0)/0.3); $("v0").style.bottom=(460*ease((t-b0+0.1)/0.6)+790)+"px";',
 '$("bar0").style.height=(430*ease((t-b0+0.1)/0.6))+"px"; $("v0").style.opacity=clamp((t-b0)/0.3); $("v0").style.bottom=(430*ease((t-b0+0.1)/0.6)+330)+"px";'),
('$("v1").style.bottom=(14+770+20)+"px";','$("v1").style.bottom=(14+310+20)+"px";'),
('show("chart",s(5),s(7),.2,t);','show("chart",s(5),E(6)+0.6,.2,t);'),
('show("end",s(7),999,.25,t);','show("end",E(6)+0.6,999,.3,t);'),
('const hide=t<S(1)-0.1||t>=s(7);','const hide=t<S(1)-0.1||t>=E(6)+0.6;'),
('$("stamp").style.transform=`translateX(-50%) rotate(-8deg)','$("stamp").style.transform=`rotate(-8deg)'),
('$("certStamp").style.transform=`translateX(-50%) rotate(-8deg)','$("certStamp").style.transform=`rotate(-8deg)'),
]
for a,b in R:
    assert a in js, a
    js=js.replace(a,b)
open('scene16.html','w').write(open('head16.html').read()+js)
T=json.loads(open('timeline.js').read().split('=',1)[1].rstrip(';\n'))[:7]
open('timeline16.js','w').write('window.TIMELINE = '+json.dumps(T)+';')
print(T[-1]['end'])
