# SaberBrain
MicroPython code for running my lightsaber.

This might not be relevant to anyone at all, or it might give you ideas on what to do.  Either way, here is the code.  Use however you wish, attributions appreciated but not required.

"Lightsaber" is probably a Lucas/Disney trademarked term or something.  I was inspired, but lets be serious, I make no claims to any intellectual property at all.

Parts List:: 
* Acrylic blade tube, endcap, "handle" parts are from https://www.thecustomsabershop.com/ The Custome Saber Shop.
* "Blade" LEDs are a pair of BTF-LIGHTING WS2812B RGB 5050SMD 1 meter, 144LED/Meter strips soldered end to end and folded back on itself.  
* "Brain" is a Raspberry Pi Pico.   
* Charging circuit is a "HiLetgo 5V 1A 18650 Lithium Battery Charging Board"   
* Batteries are a pair of 18650 3.7v 5800mAh wired in parallel.  
* a switch and a button, some wires, soldering, electrical tape, cursing and a LOT of iterations.  

lightsaber blade is on pin 15, switch is on 18, because I burned out 16 and 17 in misadventures.

I've been calling this the "PrideSaber" because of the proTrans, proQUILTBAG+ patterns in the last two.

I will post "build" images if anyone wants.  But honestly, this only exists so others can potentially learned from what I have done.

I didn't want a kit.  I wanted to build my own.  I did.  Here is the code that I used, if it helps you, that's cool.

I make no claims of being good at micropython.  But it -WORKS- in mine, so that was a success for me.
