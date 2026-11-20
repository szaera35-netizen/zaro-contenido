import base64,subprocess,os
from playwright.sync_api import sync_playwright
from PIL import Image
D="/home/claude/carrusel/"; O=D+"seg/"
b=lambda p: base64.b64encode(open(p,"rb").read()).decode()
J={w:b(f"{D}pkg_fontsource-jost/files/jost-latin-{w}-normal.woff2") for w in (400,500,600,700,800)}
logo=b(D+"logo.png")
NAVY="#30435E"; CARD="#25354D"; RED="#ED3054"; GREEN="#22C55E"
FF="".join(f"@font-face{{font-family:J;src:url(data:font/woff2;base64,{J[w]}) format('woff2');font-weight:{w}}}" for w in J)
CSS=FF+f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;font-family:J;background:{NAVY};color:#fff;position:relative;overflow:hidden}}
.lg{{position:absolute;left:96px;top:190px;width:120px;height:130px;border-radius:18px;overflow:hidden;transform:scale(1.0)}}.lg img{{width:100%;height:100%;object-fit:cover;transform:scale(1.06)}}
.w{{position:absolute;left:96px;right:96px;top:600px}}
.tag{{color:{RED};font-weight:700;font-size:34px;letter-spacing:2px;margin-bottom:24px}}
.t{{font-weight:700;font-size:84px;line-height:1.08;letter-spacing:-1px}}
.s{{font-weight:500;font-size:40px;line-height:1.4;opacity:.8;margin-top:36px}}
.r{{color:{RED}}}
.cards{{margin-top:80px;display:flex;flex-direction:column;gap:36px}}
.c{{background:{CARD};border-radius:28px;padding:40px 44px;display:flex;align-items:center;gap:40px}}
.ck{{width:100px;height:100px;border-radius:50%;flex:none;border:5px solid rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center}}
.ck.on{{background:{GREEN};border-color:{GREEN};box-shadow:0 0 0 10px rgba(34,197,94,.18)}}
.ck svg{{width:52px;height:52px}}
.c b{{display:block;font-weight:700;font-size:52px}} .c span{{font-weight:400;font-size:34px;opacity:.75}}
.c.off b,.c.off span{{opacity:.45}}
.lines{{font-weight:700;font-size:58px;line-height:1.5;margin-top:30px}}
.seal{{position:absolute;right:96px;bottom:300px;width:330px;height:330px;border-radius:50%;background:{GREEN};display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 0 16px rgba(34,197,94,.2)}}
.seal svg{{width:130px;height:130px}} .seal div{{font-weight:800;font-size:38px;letter-spacing:3px;margin-top:6px}}
.red{{background:{RED}}}
.box{{background:#fff;color:{NAVY};border-radius:24px;padding:40px 44px;margin-top:70px}}
.box small{{color:{RED};font-weight:700;font-size:28px;letter-spacing:2px}} .box p{{font-weight:700;font-size:46px;line-height:1.25;margin-top:10px}}
"""
CHK='<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
LG=f'<div class="lg"><img src="data:image/png;base64,{logo}"></div>'
def cards(items,n):
    return '<div class="cards">'+"".join(f'<div class="c {"" if i<n else "off"}"><div class="ck {"on" if i<n else ""}">{CHK if i<n else ""}</div><div><b>{a}</b><span>{s}</span></div></div>' for i,(a,s) in enumerate(items))+'</div>'
ID=[("Celular","Código SMS al número de la agencia"),("Biometría","Validación de rostro e identidad"),("Mail","Confirmación de la cuenta")]
TR=[("Cuentas de destino","Validadas con código OTP por SMS"),("Transferencias","Solo a cuentas validadas")]
S=[]  # (html, seconds, bodyclass)
S.append((f'{LG}<div class="w"><div class="t">¿Quién está<br>operando con<br><span class="r">tu usuario?</span></div></div>',1.8,""))
S.append((f'{LG}<div class="w"><div class="t">¿Quién está<br>operando con<br><span class="r">tu usuario?</span></div><div class="s">Si no lo sabés, tu agencia está expuesta.</div></div>',2.2,""))
for n in range(4):
    S.append((f'{LG}<div class="w" style="top:520px"><div class="tag">SEGURIDAD ZARO · 1/2</div><div class="t">Cada agencia valida<br>su identidad.</div>{cards(ID,n)}</div>',1,""))
for n in range(3):
    S.append((f'{LG}<div class="w" style="top:520px"><div class="tag">SEGURIDAD ZARO · 2/2</div><div class="t">Cada transferencia,<br>validada.</div>{cards(TR,n)}</div>',1,""))
S.append((f'{LG}<div class="w"><div class="t r">¿Para qué?</div><div class="lines">Tu cuenta, protegida.<br>Tu plata, a destino.<br>Nadie opera en nombre<br>de tu agencia.</div></div><div class="seal">{CHK}<div>VALIDADO</div></div>',3.4,""))
S.append((f'{LG}<div class="w"><div class="t" style="font-size:96px">Seguridad<br>desde el alta.</div><div class="box"><small>PLATAFORMA ZARO</small><p>Tu agencia, tu identidad,<br>tus operaciones protegidas.</p></div></div>',3.2,"red"))
NAR=["¿Quién está operando con tu usuario?","Si no lo sabés, tu agencia está expuesta.",
"En ZARO, cada agencia valida su identidad.","Con un código al celular de la agencia.","Con validación biométrica de rostro e identidad.","Y con confirmación por mail.",
"Y cada transferencia también se valida.","Las cuentas de destino se validan con un código único por SMS.","Y las transferencias van solo a cuentas validadas.",
"¿Para qué? Tu cuenta, protegida. Tu plata, a destino. Nadie opera en nombre de tu agencia.","ZARO. Seguridad desde el alta."]
assert len(NAR)==len(S)
V="/tmp/claude-0/-home-claude/4f7cd455-8adb-5c23-abe3-daa2e2f5b98c/scratchpad/voz/"
dur=[]
from kokoro_onnx import Kokoro
import soundfile as sf
K="/tmp/claude-0/-home-claude/4f7cd455-8adb-5c23-abe3-daa2e2f5b98c/scratchpad/ko/"
kk=Kokoro(K+"kokoro-v1.0.onnx",K+"voices-v1.0.bin")
for i,t in enumerate(NAR):
    a,sr=kk.create(t,voice="em_alex",speed=1.0,lang="es-419")
    sf.write(f"{O}n{i:02d}.wav",a,sr); dur.append(len(a)/sr)
EXTRA={len(S)-1:1.0,len(S)-2:0.6,1:0.3,5:0.4,8:0.4}
S=[(h,round(dur[i]+0.45+EXTRA.get(i,0),2),c) for i,(h,_,c) in enumerate(S)]
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1920},device_scale_factor=2)
    for i,(h,_,c) in enumerate(S):
        pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body class='{c}'>{h}</body></html>"); pg.wait_for_timeout(300)
        pg.screenshot(path=O+"big.png"); Image.open(O+"big.png").resize((1080,1920),Image.LANCZOS).convert("RGB").save(f"{O}s{i:02d}.png")
    br.close()
# xfade chain
F=0.25; ins=[]; 
for i,(_,d,_) in enumerate(S): ins+=["-loop","1","-t",str(d+F),"-i",f"{O}s{i:02d}.png"]
fc=""; prev="[0:v]"; off=0
for i in range(1,len(S)):
    off+=S[i-1][1]; tr="fade"
    fc+=f"{prev}[{i}:v]xfade=transition={tr}:duration={F}:offset={off:.2f}[v{i}];"; prev=f"[v{i}]"
fc+=f"{prev}format=yuv420p,fps=30[out]"
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[out]","-an","-c:v","libx264","-crf","18","-preset","medium","-movflags","+faststart",O+"v_tmp.mp4"],check=True)
g=Image.new("RGB",(200*len(S),356),"white")
for i in range(len(S)): g.paste(Image.open(f"{O}s{i:02d}.png").resize((195,347)),(i*200,0))
g.save(O+"sheet.jpg")

# audio
ai=[];af="";t=0.15
for i,(_,d,_) in enumerate(S):
    ai+=["-i",f"{O}n{i:02d}.wav"]; af+=f"[{i}:a]aresample=44100,adelay={int(t*1000)}|{int(t*1000)}[a{i}];"; t+=d
af+="".join(f"[a{i}]" for i in range(len(S)))+f"amix=inputs={len(S)}:normalize=0,highpass=f=70,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-16:TP=-1.5[aout]"
subprocess.run(["ffmpeg","-v","error","-y","-i",O+"v_tmp.mp4",*ai,"-filter_complex",af.replace("[0:a]","[X:a]") if False else "","-map","0:v"] if False else ["true"])
ai2=[];af2="";t=0.15
for i,(_,d,_) in enumerate(S):
    ai2+=["-i",f"{O}n{i:02d}.wav"]; af2+=f"[{i+1}:a]aresample=44100,adelay={int(t*1000)}|{int(t*1000)}[a{i}];"; t+=d
af2+="".join(f"[a{i}]" for i in range(len(S)))+f"amix=inputs={len(S)}:normalize=0,aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5[aout]"
subprocess.run(["ffmpeg","-v","error","-y","-i",O+"v_tmp.mp4",*ai2,"-filter_complex",af2,"-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",O+"seguridad_zaro_v3_voz.mp4"],check=True)
print([d for _,d,_ in S], sum(d for _,d,_ in S))
