from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "index.source.html"

MARKER = "EVENT_CLARITY_V2"


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, lambda _m: replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Could not patch {label}")
    return updated


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    if MARKER in text:
        print("Event clarity v2 already applied.")
        return

    text = text.replace(
        '#eventLabel{position:absolute;left:50%;top:45%;transform:translate(-50%,-50%);font-size:clamp(22px,7vw,54px);font-weight:950;letter-spacing:-.04em;text-align:center;opacity:0;transition:.35s;text-shadow:0 2px 18px #fff}',
        '#eventLabel{position:absolute;left:50%;top:31%;transform:translate(-50%,-50%) scale(.94);font-size:clamp(24px,7vw,58px);font-weight:950;letter-spacing:-.045em;text-align:center;opacity:0;transition:.22s;padding:10px 16px;border:1px solid #2225;border-radius:16px;background:#f4f1e8dd;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-shadow:0 12px 40px #0002;text-shadow:0 2px 12px #fff;white-space:nowrap}',
        1,
    )
    text = text.replace('#eventLabel.show{opacity:1}', '#eventLabel.show{opacity:1;transform:translate(-50%,-50%) scale(1)}', 1)

    event_geometry = r'''  // EVENT_CLARITY_V2: three unmistakable world events, all in the same neutral palette.
  var eventGroups=[],roadSlabs=[],roadPylons=[],cliffDoors=[],megaFins=[];
  var eventDark=new THREE.MeshStandardMaterial({color:0x343536,roughness:.98,metalness:.02});
  var eventMetal=new THREE.MeshStandardMaterial({color:0x777a7b,roughness:.68,metalness:.18});
  var eventLight=new THREE.MeshStandardMaterial({color:0xb8b8b4,roughness:.78,metalness:.06});

  var roadEvent=new THREE.Group();roadEvent.visible=false;scene.add(roadEvent);eventGroups.push(roadEvent);
  var roadVoid=new THREE.Mesh(new THREE.BoxGeometry(8.8,.28,31),eventDark);roadVoid.position.set(0,.23,-2);roadVoid.receiveShadow=true;roadEvent.add(roadVoid);
  for(var rs=0;rs<7;rs++){
    var slabEvent=new THREE.Mesh(new THREE.BoxGeometry(7.55,.42,4.45),roadMat);
    slabEvent.position.set(0,-5.2,10.2-rs*4.45);slabEvent.rotation.x=(rs%2===0?.62:-.58);slabEvent.rotation.z=(rs%2===0?.05:-.05);slabEvent.castShadow=true;slabEvent.receiveShadow=true;
    var slabStripe=new THREE.Mesh(new THREE.BoxGeometry(.13,.045,2.25),stripeMat);slabStripe.position.set(0,.24,0);slabEvent.add(slabStripe);
    roadEvent.add(slabEvent);roadSlabs.push(slabEvent);
  }
  for(var rp=0;rp<2;rp++){
    var roadPylon=new THREE.Mesh(new THREE.BoxGeometry(2.6,13,3.5),eventMetal);roadPylon.position.set(rp===0?-7.7:7.7,-6.4,-2);roadPylon.castShadow=true;roadPylon.receiveShadow=true;roadEvent.add(roadPylon);roadPylons.push(roadPylon);
  }
  var roadBeam=new THREE.Mesh(new THREE.BoxGeometry(18,2.0,3.0),eventLight);roadBeam.position.set(0,-4.5,-2);roadBeam.castShadow=true;roadEvent.add(roadBeam);

  var cliffEvent=new THREE.Group();cliffEvent.visible=false;scene.add(cliffEvent);eventGroups.push(cliffEvent);
  var cliffL=new THREE.Mesh(new THREE.BoxGeometry(11,13,16),gray2),cliffR=cliffL.clone();cliffL.position.set(-5.1,5.4,0);cliffR.position.set(5.1,5.4,0);cliffL.castShadow=cliffR.castShadow=true;cliffL.receiveShadow=cliffR.receiveShadow=true;cliffEvent.add(cliffL);cliffEvent.add(cliffR);cliffDoors.push(cliffL,cliffR);
  var revealCore=new THREE.Group();revealCore.position.set(0,-10,-2);cliffEvent.add(revealCore);
  var coreBody=new THREE.Mesh(new THREE.BoxGeometry(7.5,15,7),eventMetal);coreBody.castShadow=true;coreBody.receiveShadow=true;revealCore.add(coreBody);
  for(var cf=0;cf<4;cf++){var fin=new THREE.Mesh(new THREE.BoxGeometry(1.2,10,2.0),eventLight);fin.position.set((cf-1.5)*2.0,2.0,4.1);fin.rotation.z=(cf-1.5)*.035;fin.castShadow=true;revealCore.add(fin);}
  var coreEye=new THREE.Mesh(new THREE.BoxGeometry(4.8,1.0,.4),eventDark);coreEye.position.set(0,4.3,3.65);revealCore.add(coreEye);

  var megaEvent=new THREE.Group();megaEvent.visible=false;scene.add(megaEvent);eventGroups.push(megaEvent);
  var megaStructure=new THREE.Group();megaStructure.position.set(0,-22,0);megaStructure.rotation.y=.12;megaEvent.add(megaStructure);
  var megaBody=new THREE.Mesh(new THREE.BoxGeometry(28,5.5,18),eventMetal);megaBody.castShadow=true;megaBody.receiveShadow=true;megaStructure.add(megaBody);
  for(var md=0;md<3;md++){var deck=new THREE.Mesh(new THREE.BoxGeometry(34-md*4,1.2,11-md*1.5),eventLight);deck.position.set(0,6+md*5,0);deck.castShadow=true;megaStructure.add(deck);}
  for(var mf=0;mf<4;mf++){var megaFin=new THREE.Mesh(new THREE.BoxGeometry(2.0,18,3.0),eventDark);megaFin.position.set((mf<2?-1:1)*(8+(mf%2)*5),9,(mf%2===0?-5:5));megaFin.castShadow=true;megaStructure.add(megaFin);megaFins.push(megaFin);}
  var megaTop=new THREE.Mesh(new THREE.BoxGeometry(12,2.0,8),eventLight);megaTop.position.set(0,21,0);megaTop.castShadow=true;megaStructure.add(megaTop);
'''
    text = replace_once(
        text,
        r"  var eventGroup=new THREE\.Group\(\);scene\.add\(eventGroup\);var pillars=\[\];for\(var pIndex=0;pIndex<11;pIndex\+\+\)\{.*?\}\n  var petRoot",
        event_geometry + "  var petRoot",
        "event geometry",
    )

    state_code = r'''  var bubble=document.getElementById('bubble'),label=document.getElementById('eventLabel'),hint=document.getElementById('hint'),elapsed=0,eventStage=0,eventT=0,eventIndex=0,eventCooldown=0,beeps=0,lastBeep=-1,AudioCtx=window.AudioContext||window.webkitAudioContext,audio=null;
  var eventLabels=['ROAD DOES NOT EXIST','IDENTITY ERROR','SCALE BREAK'];
  var eventBubbles=['⚠ 도로가 없어!','...저게 바위야?','위쪽!'];
  var eventDistances=[27,34,44];
  function ensureAudio(){if(!AudioCtx)return;if(!audio)audio=new AudioCtx();if(audio.state==='suspended')audio.resume();}
  function beep(freq){if(!AudioCtx)return;ensureAudio();var o=audio.createOscillator(),g=audio.createGain();o.frequency.value=freq||920;g.gain.setValueAtTime(.0001,audio.currentTime);g.gain.exponentialRampToValueAtTime(.085,audio.currentTime+.01);g.gain.exponentialRampToValueAtTime(.0001,audio.currentTime+.10);o.connect(g);g.connect(audio.destination);o.start();o.stop(audio.currentTime+.11);}
  addEventListener('pointerdown',ensureAudio,{once:true});
  function placeCurrentEvent(){var g=eventGroups[eventIndex];g.visible=true;g.position.set(0,0,vehicleRoot.position.z-eventDistances[eventIndex]);}
  function startWarning(){eventStage=1;eventT=0;beeps=0;lastBeep=-1;placeCurrentEvent();bubble.textContent=eventBubbles[eventIndex];bubble.classList.add('show');}
  function startEvent(){eventStage=2;eventT=0;bubble.classList.remove('show');label.textContent=eventLabels[eventIndex];label.classList.add('show');setTimeout(function(){label.classList.remove('show');},1500);beep(eventIndex===2?540:760);}
  function finishEvent(){eventStage=3;eventT=0;eventCooldown=0;}
'''
    text = replace_once(
        text,
        r"  var bubble=document\.getElementById\('bubble'\).*?function startEvent\(\)\{.*?\}\n  var velocity=",
        state_code + "  var velocity=",
        "event state",
    )

    animate_code = r'''  var velocity=0,steer=0,clock=new THREE.Clock();
  function animate(){
    requestAnimationFrame(animate);
    var dt=Math.min(.033,clock.getDelta());elapsed+=dt;if(characterMixer)characterMixer.update(dt);
    var throttle=(keys.KeyW||keys.ArrowUp?1:0)-(keys.KeyS||keys.ArrowDown?1:0)-moveY;
    var steerInput=(keys.KeyA||keys.ArrowLeft?1:0)-(keys.KeyD||keys.ArrowRight?1:0)-moveX;
    var eventSlow=(eventStage===1||eventStage===2)?0.48:1;
    var targetVelocity=throttle*6.1*eventSlow;
    velocity=THREE.MathUtils.lerp(velocity,targetVelocity,1-Math.exp(-dt*(throttle?3.1:4.5)));
    steer=THREE.MathUtils.lerp(steer,steerInput,1-Math.exp(-dt*5.2));
    var speedRatio=Math.min(1,Math.abs(velocity)/6.1);
    vehicleRoot.rotation.y+=steer*dt*(.55+.45*speedRatio)*(velocity>=0?1:-1);
    vehicleRoot.position.x-=Math.sin(vehicleRoot.rotation.y)*velocity*dt;vehicleRoot.position.z-=Math.cos(vehicleRoot.rotation.y)*velocity*dt;vehicleRoot.position.x=THREE.MathUtils.clamp(vehicleRoot.position.x,-3.05,3.05);
    vehicleLean.rotation.z=THREE.MathUtils.lerp(vehicleLean.rotation.z,-steer*.055*speedRatio,1-Math.exp(-dt*4));vehicleLean.rotation.x=THREE.MathUtils.lerp(vehicleLean.rotation.x,-throttle*.018,1-Math.exp(-dt*4));
    wheelSpin+=velocity*dt*2.15;for(var wi=0;wi<wheels.length;wi++){var w=wheels[wi],br=w.userData.__baseRot||{x:0,y:0,z:0};w.rotation.x=br.x+wheelSpin;if(String(w.userData.steering).toLowerCase()==='true')w.rotation.y=br.y-steer*.34;}
    sun.position.x=vehicleRoot.position.x-28;sun.position.z=vehicleRoot.position.z+18;sun.target=vehicleRoot;
    if(elapsed>5)hint.style.opacity='0';if(eventStage===0&&(elapsed>11||vehicleRoot.position.z<12))startWarning();

    var petSwingZ=0,petSwingX=0;
    if(eventStage===1){eventT+=dt;petSwingZ=Math.sin(eventT*20)*(.19+eventIndex*.035);petSwingX=Math.sin(eventT*9)*.07;if(beeps<3&&eventT-lastBeep>.30){beep(900+eventIndex*80);beeps++;lastBeep=eventT;}if(eventT>2.15)startEvent();}
    else{petSwingZ=(-steer*.28)+Math.sin(elapsed*3)*.04;petSwingX=(throttle*.06)+Math.cos(elapsed*2.2)*.015;}

    if(eventStage===2){
      eventT+=dt;
      if(eventIndex===0){
        for(var sj=0;sj<roadSlabs.length;sj++){var slab=roadSlabs[sj],sl=Math.max(0,eventT-sj*.16),sh=THREE.MathUtils.smoothstep(Math.min(1,sl/.92),0,1);slab.position.y=-5.2+5.55*sh;slab.rotation.x=(sj%2===0?.62:-.58)*(1-sh);slab.rotation.z=(sj%2===0?.05:-.05)*(1-sh);}
        var ph=THREE.MathUtils.smoothstep(Math.min(1,Math.max(0,eventT-.55)/1.25),0,1);for(var pj=0;pj<roadPylons.length;pj++)roadPylons[pj].position.y=-6.4+12.9*ph;
        var bh=THREE.MathUtils.smoothstep(Math.min(1,Math.max(0,eventT-1.15)/1.15),0,1);roadBeam.position.y=-4.5+15.0*bh;
        if(eventT>4.0)finishEvent();
      }else if(eventIndex===1){
        var ch=THREE.MathUtils.smoothstep(Math.min(1,eventT/1.65),0,1);cliffDoors[0].position.x=-5.1-7.1*ch;cliffDoors[1].position.x=5.1+7.1*ch;cliffDoors[0].rotation.y=-.28*ch;cliffDoors[1].rotation.y=.28*ch;
        var coreH=THREE.MathUtils.smoothstep(Math.min(1,Math.max(0,eventT-.55)/1.65),0,1);revealCore.position.y=-10+16.2*coreH;revealCore.rotation.y=Math.sin(eventT*1.2)*.035*coreH;
        if(eventT>4.35)finishEvent();
      }else if(eventIndex===2){
        var mh=THREE.MathUtils.smootherstep(Math.min(1,eventT/2.85),0,1);megaStructure.position.y=-22+37*mh;megaStructure.rotation.y=.12-.08*mh;for(var fi=0;fi<megaFins.length;fi++)megaFins[fi].rotation.z=Math.sin(eventT*1.5+fi)*.035*mh;
        if(eventT>4.8)finishEvent();
      }
      petSwingZ+=Math.sin(eventT*9)*.045;
    }else if(eventStage===3){eventCooldown+=dt;if(eventCooldown>6.0&&eventIndex<eventGroups.length-1){eventIndex++;eventStage=0;elapsed=0;startWarning();}}

    petRig.rotation.z=THREE.MathUtils.lerp(petRig.rotation.z,petSwingZ,.15);petRig.rotation.x=THREE.MathUtils.lerp(petRig.rotation.x,petSwingX,.15);petRig.rotation.y=.18+Math.sin(elapsed*1.1)*.05;petRoot.rotation.z=Math.sin(elapsed*.5)*.03;visor.position.z=.35+Math.sin(elapsed*2.4)*.005;

    var eventActive=(eventStage===1||eventStage===2),camOffset=new THREE.Vector3(0,eventActive?3.55:2.8,eventActive?6.35:5.25);camOffset.applyAxisAngle(new THREE.Vector3(0,1,0),vehicleRoot.rotation.y+lookX*.25);var camTarget=vehicleRoot.position.clone().add(camOffset);camera.position.lerp(camTarget,1-Math.exp(-dt*(eventActive?8:6.5)));
    if(eventStage===2){var shake=Math.sin(eventT*34)*.035*Math.max(0,1-eventT/4.5);camera.position.x+=shake;camera.position.y+=Math.abs(shake)*.55;}
    camera.fov=THREE.MathUtils.lerp(camera.fov,(eventActive&&eventIndex===2)?49:57,1-Math.exp(-dt*3.2));camera.updateProjectionMatrix();
    if(eventActive){var focus=eventGroups[eventIndex].position.clone();focus.y=eventIndex===2?10:3.2;focus.z-=eventIndex===2?3:1;camera.lookAt(focus);}else{var forwardLook=new THREE.Vector3(0,.65,-6.8);forwardLook.applyAxisAngle(new THREE.Vector3(0,1,0),vehicleRoot.rotation.y);camera.lookAt(vehicleRoot.position.clone().add(forwardLook));}
    renderer.render(scene,camera);petRenderer.render(petScene,petCamera);
  }
  animate();'''
    text = replace_once(
        text,
        r"  var velocity=0,steer=0,clock=new THREE\.Clock\(\);function animate\(\)\{.*?\}animate\(\);",
        animate_code,
        "animation loop",
    )

    SOURCE.write_text(text, encoding="utf-8")
    print("Applied event clarity v2: road generation, identity reveal, scale break.")


if __name__ == "__main__":
    main()
