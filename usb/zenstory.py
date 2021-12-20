import random
import json
import pyttsx3
engine = pyttsx3.init() # object creation
engine.setProperty('rate', 125)

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1


"""VOICE"""

voices = ["englisg+f1","english+f2","english+m1","english+m3","english+m2","english_rp+m2"]

d = {
	"zen101":[
		{"title":"A cup of tea",
		"story":[
			{"voice":"1","text":"Nan-in, a Japanese master during the Meiji era (1868-1912) received a university professor who came to inquire about Zen."},
			{"voice":"1","text":"Nan-in saved tea. He poured his visitor's cup full, and then kept on pouring."},
			{"voice":"1","text":"The professor watched the overflow until he no longer could restrain himself."},
			{"voice":"2","text":"It is overfull. No more will go in"},
			{"voice":"3","text":"Like this cup,You are full of your own opinions and speculations. How can I show you Zen unless you first empty your cup?"},
			]
		},
		{"title":"Is That So?",
		"story":[
			{"voice":"1","text":"The Zen master Hakuin was praised by his neighbors as one living a pure life."},
			{"voice":"1","text":"A beautiful Japanese girl whose parents owned a food store lived near him. Suddenly, without any warning her parents discovered she was with child."},
			{"voice":"1","text":"This made her parents angry. She would not confess who the man was, but after much harassment at last named Hakuin."},
			{"voice":"1","text":"In great anger the parents went to the master. 'Is that so?' was all he would say."},
			{"voice":"1","text":"After the child was born it was brought to Hakuin. By this time he had lost his reputation, which did not trouble him, but good care of the child. He obtained milk from his neighbors and everything else the little one needed."},
			{"voice":"1","text":"A year later the girl-mother could stand it no longer. She told her parents the truth - that the real father of the child was a in the fish market."},
			{"voice":"1","text":"The mother and father of the girl at once went to Hakuin to ask his forgiveness, to apologize at length, and to get the child back again."},
			{"voice":"1","text":"Hakuin was willing. In yielding the child, all he said was"},
			{"voice":"2","text":"Is that so?"}
			]
		},
		{"title":"The Moon cannot be Stolen",
		"story":[
			{"voice":"1","text":"Ryokan, a Zen master, lived the simplest kind of life in a little hut at the foot of a mountain. One evening a thief visited the hut only to discover there was nothing in it to stea1."},
			{"voice":"1","text":"Ryokan returned and caught him."},
			{"voice":"2","text":"You may have come a long way to visit me and you should not return empty-handed. Please take my clothes as a gift."},
			{"voice":"1","text":"The thief was bewildered. He took the clothes and slunk away.Ryokan sat naked, watching the moon."},
			{"voice":"2","text":"Poor fellow, I wish I could give him this beautiful moon."},
			{"voice":"1","text":"No one can steal your beautiful heart"}
			]
		},
		{"title":"Muddy Road",
		"story":[
			{"voice":"1","text":"Tanzan and Ekido were once traveling together down a muddy road. A heavy rain was still falling."},
			{"voice":"1","text":"Coming around a bend, they met a lovely girl in a silk kimono and sash, unable to cross the intersection."},
			{"voice":"2","text":"Come on, girl"},
			{"voice":"1","text":"said Tanzan at once. Lifting her in his arms, he carried her over the mud."},
			{"voice":"1","text":"Ekido did not speak again until that night when they reached a lodging temple. Then he no longer could restrain himself."},
			{"voice":"3","text":"We monks don't go near females, especially not young and lovely ones. It is dangerous. Why did you do that?"},
			{"voice":"2","text":"I left the girl there, Are you still carrying her?"}
			]
		},
		{"title":"Learning to be Silent",
		"story":[
			{"voice":"1","text":"The pupils of the Tendai School used to study meditation before Zen entered Japan. Four of them who were intimate friends promised one another to observe seven days of silence."},
			{"voice":"1","text":"On the first day all were silent Their meditation had begun auspiciously, but when night came and the oil-lamps were growing dim one of the pupils could not help exclaiming to a servant"},
			{"voice":"2","text":"Fix those lamps"},
			{"voice":"1","text":"The second pupil was surprised to hear the first one talk."},
			{"voice":"3","text":"We are not supposed to say a word"},
			{"voice":"4","text":"You two are stupid. Why did you talk?"},
			{"voice":"1","text":"asked the third"},
			{"voice":"5","text":"I am the only one who has not talked"},
			{"voice":"1","text":"muttered the fourth pupil."}
			]
		},
		{"title":"Egotism",
		"story":[
			{"voice":"1","text":"The Prime Minister of the Tang Dynasty was a national hero for his success as both a statesman and military leader."},
			{"voice":"1","text":"But despite his fame, power, and wealth, he considered himself a humble and devout Buddhist. "},
			{"voice":"1","text":"Often he visited his favorite Zen master to study under him, and they seemed to get along very well. "},
			{"voice":"1","text":"The fact that he was prime minister apparently had no effect on their relationship, which seemed to be simply one of a revered master and respectful student."},
			{"voice":"1","text":"One day, during his usual visit, the Prime Minister asked the master,"},
			{"voice":"2","text":"Your Reverence, what is egotism according to Buddhism?"},
			{"voice":"1","text":"The master's face turned red, and in a very condescending and insulting tone of voice, he shot back,"},
			{"voice":"3","text":"What kind of stupid question is that!?"},
			{"voice":"1","text":"This unexpected response so shocked the Prime Minister that he became sullen and angry. The Zen master then smiled and said,"},
			{"voice":"3","text":"THIS, Your Excellency, is egotism."}
			]
		},
		{"title":"Full Awareness",
		"story":[
			{"voice":"1","text":"After ten years of apprenticeship, Tenno achieved the rank of Zen teacher. "},
			{"voice":"1","text":"One rainy day, he went to visit the famous master Nan-in. When he walked in, the master greeted him with a question,"},
			{"voice":"2","text":"Did you leave your wooden clogs and umbrella on the porch?"},
			{"voice":"3","text":"Yes"},
			{"voice":"2","text":"Tell me, did you place your umbrella to the left of your shoes, or to the right?"},
			{"voice":"1","text":"Tenno did not know the answer, and realized that he had not yet attained full awareness. So he became Nan-in's apprentice and studied under him for ten more years."}
			]
		},
		{"title":"The Present Moment",
		"story":[
			{"voice":"1","text":"A Japanese warrior was captured by his enemies and thrown into prison."},
			{"voice":"1","text":"That night he was unable to sleep because he feared that the next day he would be interrogated, tortured, and executed."},
			{"voice":"1","text":"Then the words of his Zen master came to him,"},
			{"voice":"2","text":"Tomorrow is not real. It is an illusion. The only reality is now."},
			{"voice":"1","text":"Heeding these words, the warrior became peaceful and fell asleep. "}
			]
		},
		{"title":"what is enlightenment?",
		"story":[
			{"voice":"1","text":"A student once asked his teacher,"},
			{"voice":"2","text":"Master, what is enlightenment?"},
			{"voice":"1","text":"The master replied,"},
			{"voice":"3","text":"When sleep, sleep. When eat, eat."}
			]
		},
		{"title":"It Will Pass",
		"story":[
			{"voice":"1","text":"A student went to his meditation teacher and said,"},
			{"voice":"2","text":"My meditation is horrible! I feel so distracted, or my legs ache, or I'm constantly falling asleep. It's just horrible!"},
			{"voice":"3","text":"It will pass,"},
			{"voice":"1","text":"the teacher said matter-of-factly."},
			{"voice":"1","text":"A week later, the student came back to his teacher."},
			{"voice":"2","text":"My meditation is wonderful! I feel so aware, so peaceful, so alive! It's just wonderful!"},
			{"voice":"3","text":"It will pass,"},
			{"voice":"1","text":"the teacher replied matter-of-factly. "}
			]
		},
		{"title":"Just Two Words",
		"story":[
			{"voice":"1","text":"There once was a monastery that was very strict. Following a vow of silence, no one was allowed to speak at all. But there was one exception to this rule."},
			{"voice":"1","text":"Every ten years, the monks were permitted to speak just two words. After spending his first ten years at the monastery, one monk went to the head monk."},
			{"voice":"2","text":"It has been ten years, What are the two words you would like to speak?"},
			{"voice":"3","text":"Bed... Hard..."},
			{"voice":"1","text":"I see,"},
			{"voice":"1","text":"Ten years later, the monk returned to the head monk's office."},
			{"voice":"2","text":"It has been ten years, What are the two words you would like to speak?"},
			{"voice":"3","text":"Food... Stinks..."},
			{"voice":"2","text":"I see,"},
			{"voice":"1","text":"Yet another ten years passed and the monk once again met with the head monk who asked,"},
			{"voice":"3","text":"What are your two words now, after these ten years?"},
			{"voice":"2","text":"I... Quit!"},
			{"voice":"3","text":"Well, I can see why, All you ever do is complain."}
			]
		},
		{"title":"Moving Mind",
		"story":[
			{"voice":"1","text":"Two men were arguing about a flag flapping in the wind."},
			{"voice":"2","text":"It's the wind that is really moving,"},
			{"voice":"1","text":"stated the first one."},
			{"voice":"3","text":"No, it is the flag that is moving,"},
			{"voice":"1","text":"contended the second."},
			{"voice":"1","text":"A Zen master, who happened to be walking by, overheard the debate and interrupted them."},
			{"voice":"4","text":"Neither the flag nor the wind is moving, It is MIND that moves."}
			]
		},
		{"title":"Be the boss",
		"story":[
			{"voice":"1","text":"A horse suddenly came galloping quickly down the road. It seemed as though the man had somewhere important to go."},
			{"voice":"1","text":"Another man, who was standing alongside the road, shouted, "},
			{"voice":"2","text":"Where are you going?"},
			{"voice":"1","text":"and the man on the horse replied,"},
			{"voice":"3","text":"I don't know! Ask the horse!"},
			{"voice":"1","text":"Explanation , The horse symbolizes our habit energy. The story explains the way we usually live,"},
			{"voice":"1","text":"at the mercy of our old habit energies which have been established not by our intentional actions, but by our surroundings and mindless activity."}
			]
		},
		{"title":"Non-judgment",
		"story":[
			{"voice":"1","text":"Once upon the time there was an old farmer who had worked his crops for many years. One day his horse ran away.Upon hearing the news, his neighbors came to visit."},
			{"voice":"2","text":"Such bad luck"},
			{"voice":"1","text":"they said sympathetically."},
			{"voice":"3","text":"Maybe,"},
			{"voice":"1","text":"the farmer replied."},
			{"voice":"1","text":"The next morning the horse returned, bringing with it three other wild horses. "},
			{"voice":"2","text":"How wonderful,"},
			{"voice":"1","text":"the neighbors exclaimed."},
			{"voice":"3","text":"Maybe,"},
			{"voice":"1","text":"the farmer replied."},
			{"voice":"1","text":"The following day, his son tried to ride one of the untamed horses, was thrown, and broke his leg. The neighbors again came to offer their sympathy on his misfortune."},
			{"voice":"3","text":"Maybe,"},
			{"voice":"1","text":"the farmer replied."},
			{"voice":"1","text":"The day after, military officials came to the village to draft young men into the army. Seeing that the son’s leg was broken, they passed him by. "},
			{"voice":"1","text":"The neighbors congratulated the farmer on how well things had turned out."},
			{"voice":"3","text":"Maybe,"},
			{"voice":"1","text":"the farmer replied."},
			{"voice":"1","text":"Explanation, There's always tomorrow. And whether the day was good or bad, there are a million effects which can arise from one event. Good and bad are interconnected. "}
			]
		},
		{"title":"Everything changes",
		"story":[
			{"voice":"2","text":"Suzuki Roshi, I've been listening to your lectures for years,"},
			{"voice":"1","text":"a student said during the question and answer time following a lecture, "},
			{"voice":"2","text":"but I just don't understand. Could you just please put it in a nutshell? Can you reduce Buddhism to one phrase?"},
			{"voice":"1","text":"Everyone laughed. Suzuki laughed."},
			{"voice":"3","text":"Everything changes,"},
			{"voice":"1","text":"he said. Then he asked for another question."}
			]
		},
		{"title":"Washing The Bowl",
		"story":[
			{"voice":"1","text":"A monk told Joshu,"},
			{"voice":"2","text":"I have just entered this monastery. I beg you to teach me."},
			{"voice":"3","text":"Have you eaten your rice porridge?"},
			{"voice":"2","text":"I have."},
			{"voice":"3","text":"Go and wash your bowl."},
			{"voice":"1","text":"At that moment the monk was enlightened."}
			]
		},
		{"title":"Nothing Exists",
		"story":[
			{"voice":"1","text":"Yamaoka Tesshu, as a young student of Zen, visited one master after another. He called upon Dokuon of Shokoku.Desiring to show his attainment, he said:"},
			{"voice":"2","text":"The mind, Buddha, and sentient beings, after all, do not exist. The true nature of phenomena is emptiness."},
			{"voice":"2","text":"There is no realization, no delusion, no sage, no mediocrity. There is no giving and nothing to be received."},
			{"voice":"1","text":"Dokuon, who was smoking quietly, said nothing. Suddenly he whacked Yamaoka with his bamboo pipe. This made the youth quite angry."},
			{"voice":"3","text":"If nothing exists,"},
			{"voice":"1","text":"inquired Dokuon,"},
			{"voice":"3","text":" where did this anger come from?"}
			]
		},
		{"title":"Time to Die",
		"story":[
			{"voice":"1","text":"Ikkyu, the Zen master, was very clever even as a boy. His teacher had a precious teacup, a rare antique. Ikkyu happened to break this cup and was greatly perplexed. "},
			{"voice":"1","text":"Hearing the footsteps of his teacher, he held the pieces of the cup behind him. When the master appeared, Ikkyu asked:"},
			{"voice":"2","text":"Why do people have to die?"},
			{"voice":"3","text":"This is natural,"},
			{"voice":"1","text":"explained the older man. "},
			{"voice":"3","text":"Everything has to die and has just so long to live."},
			{"voice":"1","text":"Ikkyu, producing the shattered cup, added"},
			{"voice":"2","text":"It was time for your cup to die."}
			]
		},
		{"title":"The Other Side",
		"story":[
			{"voice":"1","text":"One day a young Buddhist on his journey home came to the banks of a wide river. "},
			{"voice":"1","text":"Staring hopelessly at the great obstacle in front of him, he pondered for hours on just how to cross such a wide barrier."},
			{"voice":"1","text":"Just as he was about to give up his pursuit to continue his journey he saw a great teacher on the other side of the river."},
			{"voice":"1","text":"The young Buddhist yells over to the teacher, "},
			{"voice":"2","text":"Oh wise one, can you tell me how to get to the other side of this river?"},
			{"voice":"1","text":"The teacher ponders for a moment looks up and down the river and yells back,"},
			{"voice":"3","text":"My son, you are on the other side"}
			]
		},
		{"title":"Cliffhanger",
		"story":[
			{"voice":"1","text":"One day while walking through the wilderness a man stumbled upon a vicious tiger. He ran but soon came to the edge of a high cliff."},
			{"voice":"1","text":"Desperate to save himself, he climbed down a vine and dangled over the fatal precipice."},
			{"voice":"1","text":"As he hung there, two mice appeared from a hole in the cliff and began gnawing on the vine."},
			{"voice":"1","text":"Suddenly, he noticed on the vine a plump wild strawberry. He plucked it and popped it in his mouth. It was incredibly delicious!"}
			]
		}
		]
	}


with open("zenstories.json", "w") as write_file:
    json.dump(d, write_file, indent=4)
print("Done writing PrettyPrinted JSON data into file with indent=4")

# print (len(d["zen101"]))
# n = random.randint(0,len(d["zen101"]))
# print(d["zen101"][n]["title"])
# lines = d["zen101"][n]["story"]
# # print(lines)
# for i in range(len(lines)):
# 	x = int(lines[i]["voice"])
# 	# print(voices[x])
# 	engine.setProperty('voice',voices[x]) 
# 	engine.say(lines[i]["text"])

# engine.runAndWait()
# engine.stop()

# m = len(d["zen101"])
# print(m)
# sequence = [i for i in range(m)]
# print(sequence)
# random.shuffle(sequence)
# print(sequence)

# For ubuntu
# 1 install pyttsx3
# 2 install espeak