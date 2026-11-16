import re, math
from .common import item, rng, numeric_mcq
from .computer_reference import PROGRAMS

def program_variant(p,index,v):
    text=p['prompt'];code=p['code']
    if v:
        if index==0:
            a,b,c=4+v,6+v,8+v
            text=text.replace('Rs 4','Rs '+str(a)).replace('Rs 6','Rs '+str(b)).replace('Rs 8','Rs '+str(c))
            code=code.replace('* 4.0',f'* {a}.0').replace('200 +',f'{50*a} +').replace('* 6.0',f'* {b}.0').replace('500 +',f'{50*(a+b)} +').replace('* 8.0',f'* {c}.0')
        elif index==1:
            size=v+4;word=['','ABRACADABRA','MISSISSIPPI','CALCULATOR','APPLICATION'][v];ch=['','A','S','L','P'][v]
            text=text.replace('show(4)',f'show({size})').replace('show("BANANA",\'A\')',f'show("{word}",\'{ch}\')').replace('show(2.0)',f'show({v+2}.0)')
            code=code.replace('show(4)',f'show({size})').replace('show("BANANA", \'A\')',f'show("{word}", \'{ch}\')').replace('show(2.0)',f'show({v+2}.0)')
            if v%2:
                text=text.replace('Math.PI * radius * radius','2 * Math.PI * radius (circumference)')
                code=code.replace('Math.PI * radius * radius','2 * Math.PI * radius')
        elif index==2:
            orders=[('digits, uppercase letters, lowercase letters, other characters','d + " " + u + " " + l + " " + o'),('other characters, digits, lowercase letters, uppercase letters','o + " " + d + " " + l + " " + u'),('lowercase letters, other characters, uppercase letters, digits','l + " " + o + " " + u + " " + d'),('uppercase letters, digits, other characters, lowercase letters','u + " " + d + " " + o + " " + l')]
            order,expr=orders[v-1];text=text.replace('Print the four counts in that order.',f'Print the counts in this order: {order}.')
            for short,long in [('u','upper'),('l','lower'),('d','digits'),('o','other')]:expr=re.sub(r'\b'+short+r'\b',long,expr)
            code=re.sub(r'System.out.println\(upper \+.*?;',f'System.out.println({expr});',code,flags=re.S)
        elif index in (3,10,11,12):
            oldr,oldc={3:(3,4),10:(4,4),11:(3,4),12:(3,3)}[index]; nr=(4+v if index==10 else 3+v);nc=nr if index in (10,12) else 4+v
            text=text.replace(f'{oldr} by {oldc}',f'{nr} by {nc}').replace('12 integers',f'{nr*nc} integers')
            code=code.replace(f'new int[{oldr}][{oldc}]',f'new int[{nr}][{nc}]').replace(f'i < {oldr}',f'i < {nr}').replace(f'j < {oldc}',f'j < {nc}')
            if index==10:code=code.replace('a[i][3 - i]',f'a[i][{nr-1} - i]')
        elif index==4:
            n=6+v;text=text.replace('six',str(n));code=code.replace('[6]',f'[{n}]').replace('i < 6',f'i < {n}')
            if v%2:text=text.replace('ascending','descending');code=code.replace('a[j] > a[j + 1]','a[j] < a[j + 1]')
        elif index==5:
            if v%2:text=text.replace('ignoring case','with case-sensitive matching');code=code.replace('equalsIgnoreCase','equals')
            if v>=3:
                text=text.replace('first matching','last matching');code=code.replace('break;','')
            text+=f' For this set, assume 1 <= n <= {v*25}.'
        elif index==6:
            if v in (1,3):text=text.replace('beginning with a vowel','beginning with a consonant');code=code.replace('&& vowel(word.charAt(0))','&& !vowel(word.charAt(0))')
            if v in (2,3):text=text.replace('ending with a consonant','ending with a vowel');code=code.replace('&& !vowel(word.charAt(word.length() - 1))','&& vowel(word.charAt(word.length() - 1))')
            if v==4:
                text=text.replace('each word beginning with a vowel and ending with a consonant',f'each word of at least {v+1} letters beginning with a vowel and ending with a consonant');code=code.replace('word.length() > 0',f'word.length() >= {v+1}')
        elif index==7:
            div=v+2;text=f'Read a positive int n. Print Balanced if the sum of its decimal digits is divisible by {div}, otherwise print Not balanced. Use a digit-extraction loop. Do not convert the number to a String.';code=code.replace('sum % count == 0',f'sum % {div} == 0')
        elif index==8:
            n=5+v;text=text.replace('five',str(n));code=code.replace('[5]',f'[{n}]').replace('i < 5',f'i < {n}')
            if v%2:text=text.replace('descending','ascending');code=code.replace('compareTo(a[best]) > 0','compareTo(a[best]) < 0')
        elif index==9:
            old="'A','D','G','K','N','R','U','Y'";letters=[chr(ord('A')+v+i*3) for i in range(8)]
            text=text.replace('A D G K N R U Y',' '.join(letters));code=code.replace(old,','.join(repr(c) for c in letters))
        elif index==13:
            suffix=['','WAY','OY','EE','ING'][v];text=text.replace('AY',suffix);code=code.replace('"AY"',f'"{suffix}"')
        elif index==14:
            # The transformation itself differs, rather than changing the class name.
            text='Read a line of letters and spaces. Convert all letters to uppercase, then change the first letter of each word to lowercase. Preserve all spaces.'
            code=code.replace('toLowerCase()','toUpperCase()').replace('Character.toUpperCase','Character.toLowerCase')
            if v>1:
                text+=f' Process only the first {v+1} words; leave later words entirely uppercase.'
                code=code.replace('boolean start = true;', 'boolean start = true; int words = 0;').replace('result += start ? Character.toLowerCase(c) : c;',f'if(start) words++;\n                result += start && words <= {v+1} ? Character.toLowerCase(c) : c;')
        elif index==15:
            text=text.replace('at least two letters',f'at least {v+2} letters');code=code.replace('word.length() >= 2',f'word.length() >= {v+2}')
        elif index==16:
            text+=f' Then print the count of elements divisible by {v+2}.'
            pos=code.rfind('\n    }');code=code[:pos]+f'\n        int matches = 0;\n        for (int i=0;i<n;i++) if(a[i] % {v+2} == 0) matches++;\n        System.out.println(matches);'+code[pos:]
        elif index==17:
            x=1000+500*v;y=3000+1000*v;text=text.replace('1000',str(x)).replace('3000',str(y));code=code.replace('1000',str(x)).replace('3000',str(y))
        elif index==18:
            text=text.replace('x - x^2 + x^3 - ...',f'x^{v+1} - x^{v+2} + x^{v+3} - ...');code=code.replace('Math.pow(x, i)',f'Math.pow(x, i + {v})')
        elif index==19:
            text=f'Read n with 0 <= n <= 1000000000. Test whether n = k * (k + {v+1}) for a non-negative integer k. Print Matches or Not matches. Zero qualifies. Use a loop and a long variable for the products.'
            code=code.replace('(k + 1)',f'(k + {v+1})').replace('"Pronic"','"Matches"').replace('"Not pronic"','"Not matches"')
    return item(p['title'],text,p['logic']+'\nCheck: '+p['traps']+'\n\n'+code,15,id=f'computer-program-{index+1:02}-{v+1}',section=f'Priority {index+1:02} · {p["title"]}',priority=index+1,family=p['name'],code=code,category='program',evidence=p['evidence'])

def make_bank():
    bank=[]
    words=['APPLICATION','COMPUTATION','PROGRAMMING','ENCAPSULATION','CONSTRUCTOR','INHERITANCE','ALGORITHM','BINARYSEARCH','CHARACTERS','DECLARATION','POLYMORPHISM','BLUEJEDITOR','EXAMINATION','REVISION','CLASSROOM','TRANSFORMATION','STRINGMETHOD','MATHEMATICS','REPETITION','INITIALISATION']
    for v in range(1000):
        k=v%20;n=v//20;r=rng('java-a',v);a=7+3*n;b=2+n%8;word=words[n%len(words)]+(chr(65+n//20) if n>=20 else '')
        if k==19:b=n+2
        if k==0:
            prompt=f'int a={a}, b={b}; int c=a++ * 2 + --b; State c and the final values of a and b.';value=2*a+b-1;answer=f'c={value}; a={a+1}; b={b-1}. Postfix a contributes its old value; prefix --b contributes the decremented value.'
        elif k==1:
            prompt=f'Evaluate {a} / {b} + {a} % {b} in Java.';value=a//b+a%b;answer=f'{value}. Integer quotient={a//b}; remainder={a%b}.'
        elif k==2:
            lo=n%4;hi=lo+2+n%3;value=word[lo:hi];prompt=f'Give the value and length of "{word}".substring({lo},{hi}).';answer=f'"{value}", length {hi-lo}. End index excluded.'
        elif k==3:
            value=sum(range(1,b+1));prompt=f'int s={a}; for(int i=1;i<={b};i++) s+=i; Give final s and number of loop-body executions.';answer=f's={a+value}; executions={b}; increment sum={value}.';value=a+value
        elif k==4:
            prompt=f'Give output: System.out.println("{a}" + {b} + ({a} + {b}));';value=f'{a}{b}{a+b}';answer=f'{value}. String concatenation proceeds left to right; the parenthesised expression is numeric.'
        elif k==5:
            prompt=f'int[][] m=new int[{a}][{b}]; State the default value of m[0][0] and bytes for all element values, excluding overhead.';value=a*b*4;answer=f'Default=0. Element storage={a}×{b}×4={value} bytes.'
        elif k==6:
            prompt=f'Give the value and return type of Math.pow({a}, {b//2}/2).';value=float(a**((b//2)//2));answer=f'{value} (double). Integer division is completed before pow is called.'
        elif k==7:
            value=chr(65+n%26);prompt=f'Give output: System.out.println((char)({65+n%26}) + " " + ({65+n%26}+{b}));';answer=f'{value} {65+n%26+b}. Cast creates the character; the other addition is int arithmetic.';value=f'{value} {65+n%26+b}'
        elif k==8:
            prompt=f'String s="{word}"; s.toLowerCase(); System.out.print(s.charAt({n%len(word)})); Give output and explain why case is unchanged.';value=word[n%len(word)];answer=f'{value}. String is immutable; the returned lowercase String was not assigned.'
        elif k==9:
            prompt=f'int x={a}; do {{ x-={b}; }} while(x>0); State final x and body count.';count=math.ceil(a/b);value=a-count*b;answer=f'x={value}; body executes {count} times.'
        elif k==10:
            prompt=f'Write a for loop to print multiples of {b} from {b} through {b*a}, inclusive, using one loop variable.';value=None;answer=f'for(int i={b}; i<={b*a}; i+={b}) System.out.println(i);'
        elif k==11:
            prompt=f'Convert the decimal String "{a*a+b}" to an int named total, then write Java to find its square root.';value=None;answer=f'int total=Integer.parseInt("{a*a+b}");\ndouble root=Math.sqrt(total);'
        elif k==12:
            prompt=f'A sorted ascending array contains {a}, {a+b}, {a+2*b}, {a+3*b}, {a+4*b}. Trace binary search for {a+3*b}, giving mid indices until found. Use mid=(low+high)/2.';value=None;answer='Indices 2, then 3. Initially low=0, high=4; key is greater than a[2], so low=3, high=4; mid=3.'
        elif k==13:
            values=[a+b,a,a+2*b,a-b];out=values[:]
            for j in range(3):
                if out[j]>out[j+1]:out[j],out[j+1]=out[j+1],out[j]
            prompt=f'Write the array after one complete left-to-right ascending bubble-sort pass on {values}. State the number of comparisons in this pass.';value=None;answer=f'{out}; 3 comparisons. The largest value reaches the last position.'
        elif k==14:
            prompt=f'Write a method header named check{n+1} that accepts an int and a char and returns boolean. May an overload differ only in return type?';value=None;answer=f'boolean check{n+1}(int number, char code)\nNo: the parameter list must differ; return type alone does not overload a method.'
        elif k==15:
            prompt=f'Correct both errors: int[] data=new int[{a}]; for(int i=0;i<=data.length;i++) data[i]=Integer.parseInt({b});';value=None;answer=f'for(int i=0;i<data.length;i++) data[i]=Integer.parseInt("{b}");\nUse <, not <=; parseInt takes a String.'
        elif k==16:
            prompt=f'Give the values of "{word}".indexOf(\'{word[n%len(word)]}\') and "{word}".lastIndexOf(\'{word[n%len(word)]}\').';value=None;ch=word[n%len(word)];answer=f'{word.index(ch)} and {word.rindex(ch)}; indices start at zero.'
        elif k==17:
            prompt=f'class Parcel{n+1} {{ int amount; Parcel{n+1}(int amount) {{ amount=amount; }} }}\nExplain why new Parcel{n+1}({a}).amount is 0 and correct the constructor assignment.';value=None;answer='The parameter shadows the field; amount=amount only reassigns the parameter. Use this.amount=amount; the field will then receive the supplied value.'
        elif k==18:
            prompt=f'Write a conditional expression assigning fee to 0 when age<{b+8}, otherwise to {a*10}. Assume int age is declared.';value=None;answer=f'int fee = age < {b+8} ? 0 : {a*10};'
        else:
            prompt=f'int count=0; for(int i=1;i<={b};i++) for(int j=i;j<={b};j++) count++; Give final count and explain the inner bounds.';value=b*(b+1)//2;answer=f'{value}; inner iterations are {b}, {b-1}, …, 1, summing to {b}×{b+1}/2.'
        q=item(['Operators','Integer arithmetic','Strings','Loops','Concatenation','Arrays','Math methods','Characters','String immutability','Do-while','Loop rewriting','Wrapper classes','Binary search','Bubble sort','Method overloading','Error correction','String search','Constructors','Conditional operator','Nested loops'][k],prompt,answer,2,id=f'computer-a-{v+1:04}',section='Section A · 1,000 questions',family=str(k),category='short')
        if isinstance(value,(int,float)):
            mp=prompt
            if k==0:mp=prompt.split(' State ')[0]+' What is c?'
            if k==3:mp=prompt.split(' Give final ')[0]+' What is final s?'
            if k==5:mp=prompt.split(' State ')[0]+' How many bytes store the element values, excluding overhead?'
            if k==6:mp=prompt.replace('value and return type','value')
            if k==9:mp=prompt.split(' State ')[0]+' What is final x?'
            if k==19:mp=prompt.split(' Give final ')[0]+' What is final count?'
            numeric_mcq(q,value,prompt=mp)
        bank.append(q)
    bank.extend(program_variant(p,i,v) for i,p in enumerate(PROGRAMS) for v in range(5))
    return bank
