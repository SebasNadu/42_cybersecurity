
level1:	file format elf32-i386

Disassembly of section .init:

00001000 <_init>:
    1000: f3 0f 1e fb                  	endbr32
    1004: 53                           	pushl	%ebx
    1005: 83 ec 08                     	subl	$0x8, %esp
    1008: e8 b3 00 00 00               	calll	0x10c0 <__x86.get_pc_thunk.bx>
    100d: 81 c3 f3 2f 00 00            	addl	$0x2ff3, %ebx           # imm = 0x2FF3
    1013: 8b 83 f4 ff ff ff            	movl	-0xc(%ebx), %eax
    1019: 85 c0                        	testl	%eax, %eax
    101b: 74 02                        	je	0x101f <_init+0x1f>
    101d: ff d0                        	calll	*%eax
    101f: 83 c4 08                     	addl	$0x8, %esp
    1022: 5b                           	popl	%ebx
    1023: c3                           	retl

Disassembly of section .plt:

00001030 <.plt>:
    1030: ff b3 04 00 00 00            	pushl	0x4(%ebx)
    1036: ff a3 08 00 00 00            	jmpl	*0x8(%ebx)
    103c: 00 00                        	addb	%al, (%eax)
    103e: 00 00                        	addb	%al, (%eax)

00001040 <strcmp@plt>:
    1040: ff a3 0c 00 00 00            	jmpl	*0xc(%ebx)
    1046: 68 00 00 00 00               	pushl	$0x0
    104b: e9 e0 ff ff ff               	jmp	0x1030 <.plt>

00001050 <__libc_start_main@plt>:
    1050: ff a3 10 00 00 00            	jmpl	*0x10(%ebx)
    1056: 68 08 00 00 00               	pushl	$0x8
    105b: e9 d0 ff ff ff               	jmp	0x1030 <.plt>

00001060 <printf@plt>:
    1060: ff a3 14 00 00 00            	jmpl	*0x14(%ebx)
    1066: 68 10 00 00 00               	pushl	$0x10
    106b: e9 c0 ff ff ff               	jmp	0x1030 <.plt>

00001070 <__isoc99_scanf@plt>:
    1070: ff a3 18 00 00 00            	jmpl	*0x18(%ebx)
    1076: 68 18 00 00 00               	pushl	$0x18
    107b: e9 b0 ff ff ff               	jmp	0x1030 <.plt>

Disassembly of section .plt.got:

00001080 <__cxa_finalize@plt>:
    1080: ff a3 f0 ff ff ff            	jmpl	*-0x10(%ebx)
    1086: 66 90                        	nop

Disassembly of section .text:

00001090 <_start>:
    1090: f3 0f 1e fb                  	endbr32
    1094: 31 ed                        	xorl	%ebp, %ebp
    1096: 5e                           	popl	%esi
    1097: 89 e1                        	movl	%esp, %ecx
    1099: 83 e4 f0                     	andl	$-0x10, %esp
    109c: 50                           	pushl	%eax
    109d: 54                           	pushl	%esp
    109e: 52                           	pushl	%edx
    109f: e8 18 00 00 00               	calll	0x10bc <_start+0x2c>
    10a4: 81 c3 5c 2f 00 00            	addl	$0x2f5c, %ebx           # imm = 0x2F5C
    10aa: 6a 00                        	pushl	$0x0
    10ac: 6a 00                        	pushl	$0x0
    10ae: 51                           	pushl	%ecx
    10af: 56                           	pushl	%esi
    10b0: ff b3 f8 ff ff ff            	pushl	-0x8(%ebx)
    10b6: e8 95 ff ff ff               	calll	0x1050 <__libc_start_main@plt>
    10bb: f4                           	hlt
    10bc: 8b 1c 24                     	movl	(%esp), %ebx
    10bf: c3                           	retl

000010c0 <__x86.get_pc_thunk.bx>:
    10c0: 8b 1c 24                     	movl	(%esp), %ebx
    10c3: c3                           	retl
    10c4: 66 90                        	nop
    10c6: 66 90                        	nop
    10c8: 66 90                        	nop
    10ca: 66 90                        	nop
    10cc: 66 90                        	nop
    10ce: 66 90                        	nop

000010d0 <deregister_tm_clones>:
    10d0: e8 e4 00 00 00               	calll	0x11b9 <__x86.get_pc_thunk.dx>
    10d5: 81 c2 2b 2f 00 00            	addl	$0x2f2b, %edx           # imm = 0x2F2B
    10db: 8d 8a 24 00 00 00            	leal	0x24(%edx), %ecx
    10e1: 8d 82 24 00 00 00            	leal	0x24(%edx), %eax
    10e7: 39 c8                        	cmpl	%ecx, %eax
    10e9: 74 1d                        	je	0x1108 <deregister_tm_clones+0x38>
    10eb: 8b 82 ec ff ff ff            	movl	-0x14(%edx), %eax
    10f1: 85 c0                        	testl	%eax, %eax
    10f3: 74 13                        	je	0x1108 <deregister_tm_clones+0x38>
    10f5: 55                           	pushl	%ebp
    10f6: 89 e5                        	movl	%esp, %ebp
    10f8: 83 ec 14                     	subl	$0x14, %esp
    10fb: 51                           	pushl	%ecx
    10fc: ff d0                        	calll	*%eax
    10fe: 83 c4 10                     	addl	$0x10, %esp
    1101: c9                           	leave
    1102: c3                           	retl
    1103: 8d 74 26 00                  	leal	(%esi,%eiz), %esi
    1107: 90                           	nop
    1108: c3                           	retl
    1109: 8d b4 26 00 00 00 00         	leal	(%esi,%eiz), %esi

00001110 <register_tm_clones>:
    1110: e8 a4 00 00 00               	calll	0x11b9 <__x86.get_pc_thunk.dx>
    1115: 81 c2 eb 2e 00 00            	addl	$0x2eeb, %edx           # imm = 0x2EEB
    111b: 55                           	pushl	%ebp
    111c: 89 e5                        	movl	%esp, %ebp
    111e: 53                           	pushl	%ebx
    111f: 8d 8a 24 00 00 00            	leal	0x24(%edx), %ecx
    1125: 8d 82 24 00 00 00            	leal	0x24(%edx), %eax
    112b: 83 ec 04                     	subl	$0x4, %esp
    112e: 29 c8                        	subl	%ecx, %eax
    1130: 89 c3                        	movl	%eax, %ebx
    1132: c1 e8 1f                     	shrl	$0x1f, %eax
    1135: c1 fb 02                     	sarl	$0x2, %ebx
    1138: 01 d8                        	addl	%ebx, %eax
    113a: d1 f8                        	sarl	%eax
    113c: 74 14                        	je	0x1152 <register_tm_clones+0x42>
    113e: 8b 92 fc ff ff ff            	movl	-0x4(%edx), %edx
    1144: 85 d2                        	testl	%edx, %edx
    1146: 74 0a                        	je	0x1152 <register_tm_clones+0x42>
    1148: 83 ec 08                     	subl	$0x8, %esp
    114b: 50                           	pushl	%eax
    114c: 51                           	pushl	%ecx
    114d: ff d2                        	calll	*%edx
    114f: 83 c4 10                     	addl	$0x10, %esp
    1152: 8b 5d fc                     	movl	-0x4(%ebp), %ebx
    1155: c9                           	leave
    1156: c3                           	retl
    1157: 8d b4 26 00 00 00 00         	leal	(%esi,%eiz), %esi
    115e: 66 90                        	nop

00001160 <__do_global_dtors_aux>:
    1160: f3 0f 1e fb                  	endbr32
    1164: 55                           	pushl	%ebp
    1165: 89 e5                        	movl	%esp, %ebp
    1167: 53                           	pushl	%ebx
    1168: e8 53 ff ff ff               	calll	0x10c0 <__x86.get_pc_thunk.bx>
    116d: 81 c3 93 2e 00 00            	addl	$0x2e93, %ebx           # imm = 0x2E93
    1173: 83 ec 04                     	subl	$0x4, %esp
    1176: 80 bb 24 00 00 00 00         	cmpb	$0x0, 0x24(%ebx)
    117d: 75 27                        	jne	0x11a6 <__do_global_dtors_aux+0x46>
    117f: 8b 83 f0 ff ff ff            	movl	-0x10(%ebx), %eax
    1185: 85 c0                        	testl	%eax, %eax
    1187: 74 11                        	je	0x119a <__do_global_dtors_aux+0x3a>
    1189: 83 ec 0c                     	subl	$0xc, %esp
    118c: ff b3 20 00 00 00            	pushl	0x20(%ebx)
    1192: e8 e9 fe ff ff               	calll	0x1080 <__cxa_finalize@plt>
    1197: 83 c4 10                     	addl	$0x10, %esp
    119a: e8 31 ff ff ff               	calll	0x10d0 <deregister_tm_clones>
    119f: c6 83 24 00 00 00 01         	movb	$0x1, 0x24(%ebx)
    11a6: 8b 5d fc                     	movl	-0x4(%ebp), %ebx
    11a9: c9                           	leave
    11aa: c3                           	retl
    11ab: 8d 74 26 00                  	leal	(%esi,%eiz), %esi
    11af: 90                           	nop

000011b0 <frame_dummy>:
    11b0: f3 0f 1e fb                  	endbr32
    11b4: e9 57 ff ff ff               	jmp	0x1110 <register_tm_clones>

000011b9 <__x86.get_pc_thunk.dx>:
    11b9: 8b 14 24                     	movl	(%esp), %edx
    11bc: c3                           	retl
    11bd: 66 90                        	nop
    11bf: 90                           	nop

000011c0 <main>:
    11c0: 55                           	pushl	%ebp
    11c1: 89 e5                        	movl	%esp, %ebp
    11c3: 53                           	pushl	%ebx
    11c4: 81 ec 84 00 00 00            	subl	$0x84, %esp
    11ca: e8 00 00 00 00               	calll	0x11cf <main+0xf>
    11cf: 5b                           	popl	%ebx
    11d0: 81 c3 31 2e 00 00            	addl	$0x2e31, %ebx           # imm = 0x2E31
    11d6: 89 5d 80                     	movl	%ebx, -0x80(%ebp)
    11d9: c7 45 f8 00 00 00 00         	movl	$0x0, -0x8(%ebp)
    11e0: 8b 83 08 e0 ff ff            	movl	-0x1ff8(%ebx), %eax
    11e6: 89 45 86                     	movl	%eax, -0x7a(%ebp)
    11e9: 8b 83 0c e0 ff ff            	movl	-0x1ff4(%ebx), %eax
    11ef: 89 45 8a                     	movl	%eax, -0x76(%ebp)
    11f2: 8b 83 10 e0 ff ff            	movl	-0x1ff0(%ebx), %eax
    11f8: 89 45 8e                     	movl	%eax, -0x72(%ebp)
    11fb: 66 8b 83 14 e0 ff ff         	movw	-0x1fec(%ebx), %ax
    1202: 66 89 45 92                  	movw	%ax, -0x6e(%ebp)
    1206: 8d 83 16 e0 ff ff            	leal	-0x1fea(%ebx), %eax
    120c: 89 04 24                     	movl	%eax, (%esp)
    120f: e8 4c fe ff ff               	calll	0x1060 <printf@plt>
    1214: 8b 5d 80                     	movl	-0x80(%ebp), %ebx
    1217: 8d 45 94                     	leal	-0x6c(%ebp), %eax
    121a: 8d 8b 29 e0 ff ff            	leal	-0x1fd7(%ebx), %ecx
    1220: 89 0c 24                     	movl	%ecx, (%esp)
    1223: 89 44 24 04                  	movl	%eax, 0x4(%esp)
    1227: e8 44 fe ff ff               	calll	0x1070 <__isoc99_scanf@plt>
    122c: 8b 5d 80                     	movl	-0x80(%ebp), %ebx
    122f: 8d 4d 94                     	leal	-0x6c(%ebp), %ecx
    1232: 8d 55 86                     	leal	-0x7a(%ebp), %edx
    1235: 89 e0                        	movl	%esp, %eax
    1237: 89 50 04                     	movl	%edx, 0x4(%eax)
    123a: 89 08                        	movl	%ecx, (%eax)
    123c: e8 ff fd ff ff               	calll	0x1040 <strcmp@plt>
    1241: 83 f8 00                     	cmpl	$0x0, %eax
    1244: 0f 85 16 00 00 00            	jne	0x1260 <main+0xa0>
    124a: 8b 5d 80                     	movl	-0x80(%ebp), %ebx
    124d: 8d 83 2c e0 ff ff            	leal	-0x1fd4(%ebx), %eax
    1253: 89 04 24                     	movl	%eax, (%esp)
    1256: e8 05 fe ff ff               	calll	0x1060 <printf@plt>
    125b: e9 11 00 00 00               	jmp	0x1271 <main+0xb1>
    1260: 8b 5d 80                     	movl	-0x80(%ebp), %ebx
    1263: 8d 83 37 e0 ff ff            	leal	-0x1fc9(%ebx), %eax
    1269: 89 04 24                     	movl	%eax, (%esp)
    126c: e8 ef fd ff ff               	calll	0x1060 <printf@plt>
    1271: 31 c0                        	xorl	%eax, %eax
    1273: 81 c4 84 00 00 00            	addl	$0x84, %esp
    1279: 5b                           	popl	%ebx
    127a: 5d                           	popl	%ebp
    127b: c3                           	retl

Disassembly of section .fini:

0000127c <_fini>:
    127c: f3 0f 1e fb                  	endbr32
    1280: 53                           	pushl	%ebx
    1281: 83 ec 08                     	subl	$0x8, %esp
    1284: e8 37 fe ff ff               	calll	0x10c0 <__x86.get_pc_thunk.bx>
    1289: 81 c3 77 2d 00 00            	addl	$0x2d77, %ebx           # imm = 0x2D77
    128f: 83 c4 08                     	addl	$0x8, %esp
    1292: 5b                           	popl	%ebx
    1293: c3                           	retl
