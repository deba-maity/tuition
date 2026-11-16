"""Explain the actual construction used, rather than repeating the instruction."""
RULES = {
'Past passive': ('Make the original object the subject. Preserve simple past with was/were + past participle; retain the agent after by.', 'Use written, not wrote, after was.'),
'Passive to active': ('Make the by-agent the subject and the passive subject the object. Replace was/were + past participle with the simple-past main verb.', 'Do not retain was after restoring the active voice.'),
'Reported statement': ('Use a that-clause. Reporting the previous day’s words today changes I to the speaker’s pronoun, am to was, and now to then.', 'Pronouns and time words must refer to the original speaker and occasion.'),
'Reported question': ('Introduce a yes/no question with whether or if. Use statement order: subject before verb. Backshift are to was in this past-reporting context.', 'Do not write whether was I; indirect questions do not use question word order.'),
'No sooner inversion': ('At the beginning, No sooner takes auxiliary–subject inversion: had + subject + past participle. Introduce the second event with than.', 'No sooner pairs with than, not when.'),
'Hardly inversion': ('Begin Hardly had + subject + past participle; introduce the second event with when. The first event had just occurred.', 'Hardly pairs with when, not than.'),
'Correlative conjunction': ('Put not only and but also immediately before parallel elements: two adjectives, two nouns or two verb phrases.', 'Do not pair an adjective with a full clause.'),
'Too to to so that': ('Replace too + adjective + to-infinitive with so + adjective + that + subject + cannot/could not + verb. Preserve tense.', 'Too tired to continue implies inability; omitting not reverses the meaning.'),
'So that to too to': ('Replace so + adjective + that + subject + cannot with too + adjective + for + person + to-infinitive.', 'When the subject of lift differs from box, retain for + person. Do not repeat it after lift.'),
'Comparative transformation': ('Reverse the two people and express the lower degree using not as + positive adjective + as.', 'Taller than becomes not as tall as; it does not become shorter than with the same subject.'),
'Superlative transformation': ('Use No other + singular noun + is as + positive adjective + as + the original subject.', 'The superlative identifies one highest member; do not change it to one of the tallest.'),
'Unless to if': ('Unless means if not in this condition. Replace unless with if and negate its clause; leave the result clause unchanged.', 'Do not remove the negative from the result clause.'),
'If to unless': ('Replace if + negative present condition with unless + affirmative present condition.', 'Unless already supplies the negative condition; unless does not hurry reverses it.'),
'Despite to although': ('Despite takes a noun or -ing phrase; although introduces a finite clause with its own subject and verb.', 'Restore the subject and correct tense: being ill becomes she was ill.'),
'Although to in spite': ('Change the finite although-clause into a noun or -ing phrase after in spite of, keeping the same subject reference.', 'Write in spite of being, not in spite of she was.'),
'Only to none but': ('None but means no person except. Keep the original subject after none but and preserve the predicate.', 'Do not introduce a second negative into the predicate.'),
'Immediate sequence': ('The moment introduces the first event and expresses that the second followed immediately. Preserve the past tense of both.', 'Do not reverse which event happened first.'),
'Since and for': ('For gives a duration; since identifies its starting event. It is + duration + since + subject + last + simple-past verb expresses the same absence of visits.', 'Use last visited after since in this construction, not has not visited.'),
'Very few to one of': ('Very few ... as + positive adjective + as becomes one of the + superlative + plural noun.', 'Keep students plural after one of. This does not claim that the person is uniquely the most diligent.'),
'Exclamatory to assertive': ('Replace the What a ...! exclamation with a statement using normal subject–verb order and a suitable intensifier such as very.', 'Keep the same tense and remove the exclamation mark.'),
'So to such': ('So modifies an adjective; such modifies a noun phrase. Use such + a/an + adjective + singular countable noun + that.', 'Do not omit the article before a singular countable noun.'),
'Question tag': ('Repeat the statement’s auxiliary, reverse its polarity and use the subject pronoun. A positive is-statement therefore takes isn’t + pronoun.', 'Use the auxiliary from the statement, not do/does when is is already present.'),
'Unreal past condition': ('Use if + past perfect for the unreal past condition, followed by would have + past participle for its imagined result.', 'Keep would out of the if-clause; retain the negative needed by the original meaning.'),
'Emphatic auxiliary': ('Did carries past tense and requires a base-form main verb. When removing did, put the main verb in the past tense.', 'Did complete becomes completed, not complete.'),
'Agreement with both': ('Both ... and joins two subjects and takes a plural verb. As well as leaves agreement controlled by the first subject.', 'Speaks changes to speak when the subject becomes Both ... and ... .'),
}
JOIN = {
'although': ('Introduce the contrasting fact with although and retain a finite main clause.', 'Do not add but after the although-clause.'),
'because': ('Place the cause after because; the late arrival is the result of missing the bus.', 'Reversing the clauses’ logical roles changes the meaning.'),
'unless': ('Make the necessary condition affirmative after unless and keep the negative result: cannot leave unless the task is finished.', 'Avoid unless ... does not, which introduces the wrong condition.'),
'as soon as': ('Use as soon as before the first event to show that the second followed immediately.', 'Keep the sequence and original tense.'),
'who': ('Replace the repeated personal subject with who and attach the relative clause directly to that person.', 'Do not repeat she/he after who.'),
'whose': ('Whose replaces the possessive pronoun and comes directly before the possessed noun.', 'Whose advice is correct; who’s means who is or who has.'),
'where': ('Where introduces a relative clause referring to a place and replaces there.', 'Do not repeat there in the relative clause.'),
'which': ('Which refers back to the non-person noun and replaces it as the relative-clause subject.', 'Do not repeat it after which.'),
'in order to': ('Use in order to + base verb to express the purpose of the main action when the person doing both actions is the same.', 'Keep research in its base form.'),
'so that': ('Introduce the purpose with so that + subject + could/would + base verb in a past-tense context.', 'Include everyone as the subject of understand; the two clauses have different subjects.'),
'so ... that': ('Use so + adjective + that + a clause expressing the result.', 'So difficult that is correct; such difficult that is not.'),
'too ... to': ('Use too + adjective + for + person + to + base verb to express inability caused by an excessive degree.', 'Do not add cannot inside the infinitive phrase.'),
'enough to': ('Enough follows the adjective and precedes the to-infinitive.', 'Write strong enough, not enough strong.'),
'as well as': ('Connect the subjects with as well as and retain the shared predicate once.', 'In a present-tense version, the verb agrees with the first subject.'),
'not only ... but also': ('Join parallel verb phrases with not only ... but also; retain the common subject once.', 'Keep prepared and presented in parallel positions.'),
'neither ... nor': ('Use neither ... nor to combine two negative alternatives, and make the shared verb affirmative.', 'Do not retain did not after neither ... nor.'),
'either ... or': ('Use either ... or to retain the two alternatives and the modal may.', 'Do not change a possible alternative into a certainty.'),
'in spite of': ('In spite of is followed by a noun or -ing phrase expressing the contrasting circumstance.', 'Use being exhausted, not was exhausted, immediately after of.'),
'instead of': ('Instead of takes an -ing form for the rejected action; the main clause states what was actually done.', 'Do not reverse the abandoned and chosen actions.'),
'while': ('While joins two simultaneous past-continuous actions.', 'Retain was writing and was checking to preserve simultaneity.'),
'having': ('Having + past participle expresses an action completed before the main action. Its understood subject must be the main-clause subject.', 'Do not attach Having completed to a subject that did not complete the task.'),
'before': ('Use before to place checking earlier than submission.', 'Reversing the events changes the sequence.'),
'after': ('Use after before the earlier event; the main clause gives the later event.', 'Keep the explanation earlier than the discussion.'),
'if': ('An unreal past condition uses if + had + past participle and would have + past participle for the result.', 'If ... would have practised is incorrect in this construction.'),
'since': ('Here since gives a reason: loss of the original caused the use of a copy. Keep past perfect for the earlier loss.', 'Do not interpret since as a duration in this sentence.'),
}

def enrich(bank):
    for q in bank:
        family=q.get('family','')
        rule=RULES.get(family) or (JOIN.get(family[10:]) if family.startswith('Join with ') else None)
        if rule:
            q['answer']='Complete answer: '+q.get('answerText',q['answer'])+'\n\nWhy this works: '+rule[0]
            q['check']=rule[1]
    return bank
