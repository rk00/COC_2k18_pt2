# I WON ON ARXAN ONCE AGAIN 
i don't want to sound a bullshit full of himself and with an ego bigger then my house. But this was freakin epic once again

### Now it's up to you folks!
Recently, i found out that some people around the world love to use my finished work to earn moneys, other one got stuffs up
thanks to this free work - and suddenly when i pop to them asking info about their "awesome stuffs" they just ask me "hey... who the fuck are you"...
not that all the stuffs up are actually up mostly thanks to my work and the work of another couple of guys that i know and chat with time to time but.. 
let's see what those fellas can do without the things ready on an open repository.
Those sets of scripts are everything you need to reach the solution of the puzzle. There is a chain of posts on my blog, and one will come as well documenting this works and the methodologies used to reach what i was needed to reach


- use ``att.py`` which will use ``att_coc.js`` to kang memory dumps from your device. 
#### this is old. kept for backlog
- (move libg to root folder -> md5: 0fcad6e1094043d284e68cf80ee0d6f2) <-- this is not needed anymore. library is now kanged from memory as well.
- edit ``emu.py`` to setup lib base and registers according to the output of frida script
- get a cup of coffee and let the emulation run
#### this is actual
- we are dumping 2 stages. Whatever happens before the encryption of the payload and whatever happens right at the beginning of the encryption
- we are going to use 2 different emulators for the 2 stages. 
- the output of the frida scripts will print: 
a) the base of the lib, copy it to ``emu_base``
b) the nonce
c) the public key
d) the registers for stage1 (copy them to ``emu_stage_1`` if you want to run stage1)
e) the registers for stage2 (copy them to ``emu_stage_2`` if you want to run stage2)
f) the registers for stage3 (copy them to ``emu_stage_3`` if you want to run stage2)
g) the encrypted login to compare

#### stages
1) build of private key
2) shared key gen
3) encryption of login
- nonce should happens either in stage 1 or 2 (still needs to be figured out)

#### Hey dudes at SC!?

- I told you once that ``/dev/urandom`` will kill you one day. That's the day :D
- We once spoke together about replacing plt with svc (supervisorcall) inline instructions. This gave us some fun scripting an inline detection to any SVC instruction (which is kept priv8 from @enovella actually) - but.... no Arxan over there, on my side, was a matter of hooking an in-line instruction instead of a PLT. 
- About this last point, you told me that it's not that usefull since i'm going to cleanup hooking instruction before the crc cycle. That's very correct but would turn it way funny and anyway... we should discuss some smarter way to at least prevent an hook to the Hello message (which is the starts of any debugging things i built since i begin).

#### Once again 

- Russians, French and Chinese people keeps pwning you with 4 lines which just consists in jumping the encryption and fucking it out. There are hundred ways to prevent this. Making sure a specific instruction got hit at least once should be easy, but also easily crackable. I'm sure you know how to make this harder giving the right focus on that case.
- I dont give a damn 'bout the effort I'll be happy once I (and my eyes needs to) see 1500/5000/2500000 py lines that replicate encryption logic.
- Arxan is keep pwned in lot of different funny ways -> ``att_coc_flow`` and enjoy the correct flow of execution. String encryption is done. CRC persist just because no one given a real damn about it :D
- GDB can be attached using frida api Process.isDebuggerAttached in a while true until it's attached.
- I got no help. But... i know you guys since 1 year (or more). Public key and nonce are still there which make me think that i'm stil dealing with a sodium based encryption and you had lot of fun changing lines and numbers all around (which is very smart imho and still need a full re-implementation instead of a single byte change)

