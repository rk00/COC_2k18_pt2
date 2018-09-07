**WIP WIP** 

- use ``att.py`` which will use ``att_coc.js`` to kang memory dumps from your device. 
- move libg to root folder -> md5: 0fcad6e1094043d284e68cf80ee0d6f2
- edit ``emu.py`` to setup lib base and registers according to the output of frida script
- get a cup of coffee and let it run emulation

the last time i pushed the finished implementation, this time, I push the wip so the guys at the crew can follow the works.
I'm not sure i'll win this, this time. But im going to do my best as usual!

#### Hey dudes at SC!?

- I told you once that ``/dev/urandom`` will kill you one day. That's the day :D
- We once spoke together about replacing plt with svc (supervisorcall) inline instructions. This gave us some fun scripting an inline detection to any SVC instruction (which is kept priv8 from @enovella actually) - but.... no Arxan over there, on my side, was a matter of hooking an in-line instruction instead of a PLT. 
- About this last point, you told me that it's not that usefull since i'm going to cleanup hooking instruction before the crc cycle. That's very correct but would turn it way funny and anyway... we should discuss some smarter way to at least prevent an hook to the Hello message (which is the starts of any debugging things i built since i begin).

#### Once again 

- Russians, French and Chinese people keeps pwning you with 4 lines which just consists in jumping the encryption and fucking it out. There are hundred ways to prevent this. Making sure a specific instruction got hit at least once should be easy, but also easily crackable. I'm sure you know how to make this harder giving the right focus on that case.
- I dont give a damn. I'll be happy once I see 1500/5000/2500000 py lines that replicate encryption logic.
- Arxan is keep pwned in lot of different funny ways -> ``att_coc_flow`` and enjoy the correct flow of execution. String encryption is done. CRC persist just because no one given a real damn about it :D
- GDB can be attached using frida api Process.isDebuggerAttached in a while true until it's attached.
- I got no help. But... i know you guys since 1 year (or more). Public key and nonce are still there which make me think that i'm stil dealing with a sodium based encryption and you had lot of fun changing lines and numbers all around (which is very smart imho and still need a full re-implementation instead of a single byte change)

