from .common import rng
ROWS={
'histciv':'''What is a bicameral legislature? Name the two Houses of India’s Parliament.|A legislature with two chambers; Lok Sabha and Rajya Sabha.
Who presides over the Lok Sabha? Who is the ex-officio Chairman of the Rajya Sabha?|Speaker; Vice-President respectively.
State the normal term of the Lok Sabha and the term of a Rajya Sabha member.|Five years; six years respectively.
What is collective responsibility of the Union Council of Ministers? To which House is it owed?|The ministry stands or falls together as a body and must retain the confidence of the Lok Sabha.
State one ordinary executive appointment power and one legislative function of the President.|Appoints the Prime Minister; summons Parliament/gives assent to bills. Accept other correct ordinary powers with constitutional qualifications.
Distinguish the Council of Ministers from the Cabinet.|The Council includes all categories of ministers; the Cabinet is the smaller senior decision-making body within it.
What is judicial review? Name one court that exercises it.|Examination of law/executive action for constitutional validity; Supreme Court or a High Court.
What is the purpose of habeas corpus? What can the court require?|Protection against unlawful detention; production of the detained person and justification of detention, with release if unlawful.
Name the immediate military grievance of 1857 and the place where the major outbreak began on 10 May.|Greased Enfield cartridges; Meerut.
What was the Doctrine of Lapse? Name the Governor-General associated with it.|Annexation of certain states when a ruler died without a recognised natural heir under the policy; Dalhousie.
State two major administrative consequences of the 1857 uprising.|Company rule ended and Crown rule began; office of Secretary of State for India created. Accept appropriate army reorganisation or changed princely-state policy as distinct consequences.
Give two constitutional methods used by Early Nationalists.|Petitions/memorials; speeches, resolutions or reasoned appeals. Award two distinct methods.
Name two Assertive Nationalist leaders.|Bal Gangadhar Tilak, Bipin Chandra Pal, Lala Lajpat Rai: any two.
State one objective each of Swadeshi and Boycott.|Swadeshi promoted indigenous production/use; Boycott rejected foreign goods/institutions as a means of pressure and self-reliance.
Give the year and place of the Muslim League’s founding.|1906; Dacca/Dhaka.
Name the pact of 1916 between Congress and the Muslim League and state one significance.|Lucknow Pact; joint constitutional demands/cooperation between the organisations, including an agreed representation scheme.
Give two immediate causes contributing to the Non-Cooperation Movement.|Rowlatt repression/Jallianwala Bagh; Khilafat grievances. Accept two clearly different syllabus causes.
Why was Non-Cooperation withdrawn in 1922? Name the incident.|Chauri Chaura violence, including burning of a police station; Gandhi judged the movement insufficiently disciplined in non-violence.
What law did the Dandi March challenge, and in which year?|The British salt monopoly/tax law; 1930.
State the year of Quit India and the central demand of the movement.|1942; end British rule/withdraw from India.
Name the principal leader associated with the INA’s later campaign and give one objective.|Subhas Chandra Bose; armed struggle to liberate India from British rule.
State two provisions of the Indian Independence Act 1947.|Creation of India and Pakistan as independent dominions; British paramountcy over princely states ended. Accept other correct distinct provisions.
Name the immediate trigger of World War I and the treaty imposed on Germany after it.|Assassination of Archduke Franz Ferdinand at Sarajevo; Treaty of Versailles.
Name the dictator associated with Fascism in Italy and the dictator associated with Nazism in Germany.|Benito Mussolini; Adolf Hitler.
What was appeasement? Give one pre-war example.|Concessions to an aggressor in the hope of avoiding war; Munich settlement allowing German annexation of the Sudetenland.
Name the 1939 invasion that triggered war in Europe and two countries that then declared war on Germany.|Invasion of Poland; Britain and France.
Name two permanent members of the UN Security Council.|Any two of China, France, Russia, United Kingdom, United States.
State two principal aims of the UN.|Maintain international peace/security; develop friendly relations/cooperation and promote human rights. Award two distinct aims.
Give the chief fields of work of WHO and UNESCO.|WHO: health; UNESCO: education, science and culture.
Distinguish non-alignment from isolation.|Non-alignment means independent judgement outside rival military blocs; isolation means withdrawal from international engagement. NAM favours active engagement rather than isolation.''',
'phy':'''Define moment of a force and give its SI unit.|Force × perpendicular distance from the pivot; newton metre (N m).
State two conditions for equilibrium of a rigid body.|Resultant force zero; resultant moment about any point zero.
Define a couple and state its main effect.|Two equal opposite parallel forces with distinct lines of action; a turning effect with zero resultant force.
Define power and give its SI unit.|Rate of doing work/energy transfer; watt.
Distinguish kinetic and gravitational potential energy.|Energy due to motion, ½mv²; energy due to height in a gravitational field, mgh near Earth.
Define mechanical advantage and velocity ratio.|MA=load/effort; VR=distance moved by effort/distance moved by load.
Can a real machine have efficiency above 100 percent? Give a reason.|No; useful energy output cannot exceed total energy input. Real losses reduce efficiency below unity.
State both conditions for total internal reflection.|Light must go from optically denser to rarer medium; angle of incidence must exceed the critical angle.
Define refractive index in terms of speeds and state its unit status.|n=c/v for light speed in vacuum divided by that in the medium; dimensionless.
State the SI unit of lens power and the sign of a concave lens’s power.|Dioptre (D); negative.
How does increasing frequency affect sound pitch? How does increasing amplitude affect loudness?|Higher frequency raises pitch; greater amplitude increases loudness, other conditions fixed.
Why is echo distance calculated using half the total travel time times speed?|The measured delay includes travel to the reflector and back; d=vt/2.
State the relation between wave speed, frequency and wavelength. Give the SI unit of wavelength.|v=fλ; metre.
State Ohm’s law including a condition for validity.|At constant temperature/physical conditions, current is proportional to potential difference; V=IR.
State which electrical quantity is common to resistors in series and which is common to parallel branches.|Series: current. Parallel branches: potential difference.
Why is a fuse placed in the live wire in series with an appliance?|Excess current melts the fuse and interrupts the live supply to the appliance, reducing overheating/fire risk.
What is the purpose of earthing a metal appliance casing?|Provides a low-resistance path for fault current, keeping the case near earth potential and helping the protective device disconnect the supply.
What is one kilowatt-hour? Express it in joules.|Energy used by 1 kW in 1 h; 3.6×10⁶ J.
Why cannot steady DC operate a transformer continuously in the ordinary way?|Steady DC produces no continuously changing magnetic flux, so no sustained induced secondary emf; switching transients are different.
State the turn-voltage relation for an ideal transformer and the condition for stepping down.|Vs/Vp=Ns/Np; step-down when Ns<Np.
Define specific heat capacity and give its SI unit.|Heat required to raise 1 kg of a substance by 1 K; J kg⁻¹ K⁻¹.
Why can temperature stay constant while ice melts despite heat input?|Energy is absorbed as latent heat to change the state rather than increase the temperature under the stated melting conditions.
State the changes in mass number and atomic number in alpha emission.|Mass number decreases by 4; atomic number decreases by 2.
State the changes in mass number and atomic number in beta-minus emission.|Mass number unchanged; atomic number increases by 1.
Why is gamma radiation undeflected by electric and magnetic fields?|It is uncharged electromagnetic radiation, so it experiences no charge-based deflecting force.'''
}
def short_questions(sid,n,count):
    pool=[]
    for row in ROWS[sid].splitlines():
        prompt,answer=row.split('|',1);pool.append(dict(prompt=prompt,answer=answer,marks=2))
    rng(sid+'shorts',n).shuffle(pool)
    return pool[:count]
