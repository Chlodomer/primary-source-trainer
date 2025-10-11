"""
Scenario generator for historically plausible early medieval source chains.
Generates 10 diverse scenarios with varying complexity and transmission patterns.
"""

from models import Scenario, Event, SourceNode, Edge, Topic, TransmissionStep


def generate_scenarios() -> list[Scenario]:
    """Generate all 10 scenarios for the training session."""
    return [
        generate_lindisfarne_raid(),
        generate_justinian_plague(),
        generate_merovingian_succession(),
        generate_iconoclasm_debate(),
        generate_donation_of_pepin(),
        generate_lombard_invasion(),
        generate_visigothic_conversion(),
        generate_battle_of_tours(),
        generate_gregory_of_tours(),
        generate_byzantine_embassy(),
    ]


def generate_lindisfarne_raid() -> Scenario:
    """Scenario 1: The Viking raid on Lindisfarne (793 CE) - Easy difficulty."""
    return Scenario(
        id="scenario_1_lindisfarne",
        difficulty="easy",
        event=Event(
            id="evt_lindisfarne_793",
            title="Viking Raid on Lindisfarne",
            year=793,
            place="Northumbria, England",
            description="Norse raiders attacked the monastery at Lindisfarne, marking the beginning of the Viking Age in England.",
            image_url=None,  # Image temporarily disabled
            composition_info="Alcuin's letter represents immediate Northumbrian clerical reaction, while the Anglo-Saxon Chronicle compiled memories from lost oral traditions and earlier annals a century later. Simeon of Durham synthesized lost northern chronicles over 300 years after the raid, showing how monastic memory preserved Viking-age trauma through now-vanished intermediaries."
        ),
        nodes=[
            SourceNode(
                id="n1",
                type="text",
                title="Letter from Alcuin to King Æthelred",
                author_role="contemporary scholar (witness to aftermath)",
                year=793,
                place="Frankish court",
                extant=True,
                description="Alcuin, a Northumbrian scholar at Charlemagne's court, writes about the raid shortly after hearing news."
            ),
            SourceNode(
                id="lost_oral",
                type="text",
                title="Oral Traditions & Earlier Annals",
                author_role="various storytellers and scribes",
                year=850,
                place="England",
                extant=False,
                description="Lost oral traditions and earlier written annals about the raid that no longer survive."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Anglo-Saxon Chronicle Entry",
                author_role="monastic compiler",
                year=890,
                place="Wessex",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: oral traditions and earlier annals", year=850, type="compilation")
                ],
                description="Compiled nearly a century later from lost oral traditions and earlier written records that no longer survive. This makes the Chronicle the closest extant source for that transmission chain."
            ),
            SourceNode(
                id="lost_chronicle",
                type="text",
                title="Lost Northumbrian Chronicle",
                author_role="northern monastic scribe",
                year=900,
                place="Northumbria",
                extant=False,
                description="A lost northern chronicle that recorded the raid and its aftermath."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="Simeon of Durham's History",
                author_role="medieval historian",
                year=1104,
                place="Durham, England",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: Northumbrian chronicle", year=900, type="summary"),
                    TransmissionStep(via="lost: earlier compilation", year=1000, type="copy")
                ],
                description="12th-century monk writing 300+ years after the raid, based on lost Northumbrian chronicles that no longer survive. This makes Simeon's work the closest extant source for that northern chronicle tradition."
            ),
        ],
        edges=[
            Edge(from_id="evt_lindisfarne_793", to="n1", kind="contemporary_witness"),
            Edge(from_id="evt_lindisfarne_793", to="lost_oral", kind="oral_transmission"),
            Edge(from_id="lost_oral", to="n2", kind="compilation"),
            Edge(from_id="evt_lindisfarne_793", to="lost_chronicle", kind="early_record"),
            Edge(from_id="lost_chronicle", to="n3", kind="derivative_summary"),
        ],
        topics=[
            Topic(id="t_event", label="The raid itself (793 CE)", anchor="evt_lindisfarne_793"),
            Topic(id="t_memory", label="9th-century Anglo-Saxon memory of Viking raids", anchor="n2"),
        ]
    )


def generate_justinian_plague() -> Scenario:
    """Scenario 2: Justinianic Plague (541-542 CE) - Medium difficulty."""
    return Scenario(
        id="scenario_2_plague",
        difficulty="medium",
        event=Event(
            id="evt_plague_541",
            title="Justinianic Plague in Constantinople",
            year=541,
            place="Constantinople",
            description="First pandemic of bubonic plague in the Mediterranean world.",
            image_url=None,  # Image temporarily disabled
            composition_info="Procopius documented the pandemic firsthand as an eyewitness. Michael the Syrian's 12th-century Syriac compilation preserves fragments from lost eyewitness accounts (including John of Ephesus) through a long transmission chain. Modern scholarship analyzes both ancient sources."
        ),
        nodes=[
            SourceNode(
                id="n1",
                type="text",
                title="Procopius' History of the Wars",
                author_role="eyewitness historian",
                year=545,
                place="Constantinople",
                extant=True,
                description="Procopius was in Constantinople during the plague and describes it firsthand."
            ),
            SourceNode(
                id="lost_john",
                type="text",
                title="John of Ephesus' Lost Eyewitness Account",
                author_role="eyewitness historian",
                year=580,
                place="Ephesus",
                extant=False,
                description="Lost eyewitness account by John of Ephesus, who survived the plague and documented it firsthand. His work no longer survives but was preserved through later Syriac compilations."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Michael the Syrian's Chronicle (Syriac)",
                author_role="medieval chronicler",
                year=1195,
                place="Antioch",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: John of Ephesus' eyewitness account", year=580, type="summary"),
                    TransmissionStep(via="lost: intermediate Syriac chronicle", year=800, type="translation")
                ],
                description="12th-century Syriac chronicle written 650+ years after the plague, preserving excerpts from earlier sources."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="Modern epidemiological study (2020)",
                author_role="modern historian/scientist",
                year=2020,
                place="Multiple universities",
                extant=True,
                transmission=[
                    TransmissionStep(via="Procopius (extant)", year=545, type="summary"),
                    TransmissionStep(via="Michael the Syrian (extant)", year=1195, type="summary")
                ],
                description="Scholarly article analyzing OTHER EXTANT ancient sources about the plague (Procopius and Michael)."
            ),
        ],
        edges=[
            Edge(from_id="evt_plague_541", to="n1", kind="eyewitness"),
            Edge(from_id="evt_plague_541", to="lost_john", kind="eyewitness"),
            Edge(from_id="lost_john", to="n2", kind="transmission_via_lost"),
            Edge(from_id="n1", to="n3", kind="modern_analysis"),
            Edge(from_id="n2", to="n3", kind="modern_analysis"),
        ],
        topics=[
            Topic(id="t_event", label="The plague itself (541-542 CE)", anchor="evt_plague_541"),
            Topic(id="t_historiography", label="Modern historiography of ancient plagues", anchor="n3"),
        ]
    )


def generate_merovingian_succession() -> Scenario:
    """Scenario 3: Merovingian succession crisis (511 CE) - Easy."""
    return Scenario(
        id="scenario_3_succession",
        difficulty="easy",
        event=Event(
            id="evt_clovis_death_511",
            title="Death of Clovis and division of Frankish kingdom",
            year=511,
            place="Paris",
            description="King Clovis dies; his kingdom is divided among his four sons.",
            image_url=None,  # Image temporarily disabled
            composition_info="Gregory of Tours wrote the only surviving narrative 70 years later, relying on lost oral traditions and court records. Contemporary coins like Theuderic's solidus provide independent material evidence."
        ),
        nodes=[
            SourceNode(
                id="lost_court_records",
                type="text",
                title="Lost Merovingian Court Records",
                author_role="court scribe",
                year=540,
                place="Paris/Frankish courts",
                extant=False,
                description="Lost official court records and oral traditions from the Merovingian courts documenting Clovis' succession. These records no longer survive but were used by Gregory of Tours in his compilation."
            ),
            SourceNode(
                id="n1",
                type="text",
                title="Gregory of Tours' Histories (Book II)",
                author_role="bishop-historian",
                year=580,
                place="Tours",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: oral traditions and court records", year=540, type="compilation")
                ],
                description="Written 70 years after the event, compiling information from earlier sources that no longer survive."
            ),
            SourceNode(
                id="n2",
                type="artifact",
                title="Coin of Clovis' son Theuderic",
                author_role="royal mint",
                year=515,
                place="Metz",
                extant=True,
                description="Physical coin minted just 4 years after Clovis' death, showing one of the successor kings."
            ),
        ],
        edges=[
            Edge(from_id="evt_clovis_death_511", to="lost_court_records", kind="official_record"),
            Edge(from_id="lost_court_records", to="n1", kind="derivative"),
            Edge(from_id="evt_clovis_death_511", to="n2", kind="contemporary_artifact"),
        ],
        topics=[
            Topic(id="t_event", label="Clovis' death and succession (511 CE)", anchor="evt_clovis_death_511"),
        ]
    )


def generate_iconoclasm_debate() -> Scenario:
    """Scenario 4: Byzantine Iconoclasm (726 CE) - Hard."""
    return Scenario(
        id="scenario_4_iconoclasm",
        difficulty="hard",
        event=Event(
            id="evt_iconoclasm_726",
            title="Emperor Leo III orders removal of icons",
            year=726,
            place="Constantinople",
            description="Byzantine Emperor Leo III initiates iconoclasm, banning religious images.",
            image_url=None,  # Image temporarily disabled
            composition_info="The original imperial edict is lost; our knowledge comes from Theophanes' hostile 9th-century chronicle (based on the lost edict) and Pope Gregory II's immediate protest letter. Modern scholarship analyzes these surviving sources."
        ),
        nodes=[
            SourceNode(
                id="lost_edict",
                type="text",
                title="Lost Imperial Edict Against Icons",
                author_role="imperial scribe",
                year=726,
                place="Constantinople",
                extant=False,
                description="Lost official imperial edict issued by Emperor Leo III ordering the removal of religious icons. The original document no longer survives but was summarized by later chroniclers like Theophanes."
            ),
            SourceNode(
                id="n1",
                type="text",
                title="Theophanes' Chronicle",
                author_role="monastic chronicler (iconodule)",
                year=815,
                place="Constantinople",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: Imperial edict", year=726, type="summary")
                ],
                description="Pro-icon monk writing 90 years later, preserving information from the now-lost imperial edict."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Pope Gregory II's Letter to Leo III",
                author_role="pope (contemporary opponent)",
                year=727,
                place="Rome",
                extant=True,
                description="Letter condemning iconoclasm, written immediately after hearing of the edict."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="Modern art history essay on Byzantine iconoclasm",
                author_role="modern scholar",
                year=2018,
                place="Oxford",
                extant=True,
                transmission=[
                    TransmissionStep(via="Theophanes (extant)", year=815, type="summary"),
                    TransmissionStep(via="Gregory II (extant)", year=727, type="summary")
                ],
                description="Scholarly article analyzing OTHER EXTANT sources (Theophanes and Gregory)."
            ),
        ],
        edges=[
            Edge(from_id="evt_iconoclasm_726", to="lost_edict", kind="official_decree"),
            Edge(from_id="lost_edict", to="n1", kind="hostile_summary"),
            Edge(from_id="evt_iconoclasm_726", to="n2", kind="contemporary_reaction"),
            Edge(from_id="n1", to="n3", kind="scholarly_analysis"),
            Edge(from_id="n2", to="n3", kind="scholarly_analysis"),
        ],
        topics=[
            Topic(id="t_event", label="Leo III's iconoclasm decree (726 CE)", anchor="evt_iconoclasm_726"),
            Topic(id="t_reception", label="9th-century Byzantine memory of iconoclasm", anchor="n1"),
            Topic(id="t_historiography", label="Modern art historical interpretation", anchor="n3"),
        ]
    )


def generate_donation_of_pepin() -> Scenario:
    """Scenario 5: Donation of Pepin (756 CE) - Medium."""
    return Scenario(
        id="scenario_5_donation",
        difficulty="medium",
        event=Event(
            id="evt_donation_756",
            title="Pepin III donates territory to the Papacy",
            year=756,
            place="Pavia, Italy",
            description="Frankish king grants lands to the Pope, creating the Papal States.",
            image_url=None,  # Image temporarily disabled
            composition_info="The Liber Pontificalis provides the papal perspective written within a year, while Frankish court annals offer a northern version compiled decades later. The forged Donation of Constantine (c. 850) retrospectively justified papal territorial claims by inventing a Constantinian precedent."
        ),
        nodes=[
            SourceNode(
                id="n1",
                type="text",
                title="Liber Pontificalis entry for Pope Stephen II",
                author_role="papal biographer",
                year=757,
                place="Rome",
                extant=True,
                description="Official papal biography written shortly after the donation."
            ),
            SourceNode(
                id="lost_frankish_court",
                type="text",
                title="Lost Frankish Court Records",
                author_role="court scribe",
                year=760,
                place="Frankish court",
                extant=False,
                description="Lost official court records from Pepin III's reign documenting the territorial donation to the papacy. These records no longer survive but were compiled into the Royal Frankish Annals."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Royal Frankish Annals",
                author_role="court annalist",
                year=790,
                place="Frankish court",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: court records", year=760, type="compilation")
                ],
                description="Frankish perspective compiled 30+ years later from lost court records that no longer survive."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="Forged 'Donation of Constantine'",
                author_role="papal forger",
                year=850,
                place="Rome",
                extant=True,
                description="Fake document claiming Constantine gave Rome to the papacy, created to justify Pepin's donation."
            ),
        ],
        edges=[
            Edge(from_id="evt_donation_756", to="n1", kind="official_record"),
            Edge(from_id="evt_donation_756", to="lost_frankish_court", kind="court_record"),
            Edge(from_id="lost_frankish_court", to="n2", kind="compilation"),
            Edge(from_id="n1", to="n3", kind="inspired_forgery"),
        ],
        topics=[
            Topic(id="t_event", label="The donation itself (756 CE)", anchor="evt_donation_756"),
            Topic(id="t_forgery", label="9th-century papal propaganda about imperial donations", anchor="n3"),
        ]
    )


def generate_lombard_invasion() -> Scenario:
    """Scenario 6: Lombard invasion of Italy (568 CE) - Easy."""
    return Scenario(
        id="scenario_6_lombards",
        difficulty="easy",
        event=Event(
            id="evt_lombards_568",
            title="Lombards invade Italy under King Alboin",
            year=568,
            place="Northern Italy",
            description="Germanic Lombards cross the Alps and conquer much of Italy.",
            image_url=None,  # Image temporarily disabled
            composition_info="Marius of Aventicum's brief contemporary notice from neighboring Burgundy contrasts with Paul the Deacon's detailed 8th-century history. Paul wrote 220 years later at Monte Cassino, compiling Lombard oral traditions into literary Latin for a Carolingian audience."
        ),
        nodes=[
            SourceNode(
                id="n1",
                type="text",
                title="Paul the Deacon's History of the Lombards",
                author_role="Lombard historian-monk",
                year=790,
                place="Monte Cassino",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: oral traditions", year=650, type="compilation")
                ],
                description="Written 220 years after the invasion, based on lost Lombard oral traditions that no longer survive."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Marius of Aventicum's Chronicle",
                author_role="bishop-chronicler",
                year=581,
                place="Burgundy",
                extant=True,
                description="Brief contemporary mention of the invasion from a neighboring region."
            ),
        ],
        edges=[
            Edge(from_id="evt_lombards_568", to="n2", kind="contemporary_notice"),
            Edge(from_id="evt_lombards_568", to="lost_oral", kind="oral_tradition"),
            Edge(from_id="lost_oral", to="n1", kind="literary_compilation"),
        ],
        topics=[
            Topic(id="t_event", label="The invasion itself (568 CE)", anchor="evt_lombards_568"),
        ]
    )


def generate_visigothic_conversion() -> Scenario:
    """Scenario 7: Visigothic conversion to Catholicism (589 CE) - Medium."""
    return Scenario(
        id="scenario_7_conversion",
        difficulty="medium",
        event=Event(
            id="evt_conversion_589",
            title="King Reccared converts Visigoths from Arianism to Catholicism",
            year=589,
            place="Toledo, Spain",
            description="Third Council of Toledo marks official conversion of Visigothic kingdom.",
            image_url=None,  # Image temporarily disabled
            composition_info="The official Acts of the Council provide the institutional record, while Bishop John of Biclar's contemporary chronicle offers an eyewitness account. Isidore of Seville later synthesized both sources in his History of the Goths (625), shaping how early medieval Iberia understood its own conversion."
        ),
        nodes=[
            SourceNode(
                id="n1",
                type="text",
                title="Acts of the Third Council of Toledo",
                author_role="conciliar scribe",
                year=589,
                place="Toledo",
                extant=True,
                description="Official record of the church council."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="John of Biclar's Chronicle",
                author_role="bishop (participant)",
                year=590,
                place="Iberia",
                extant=True,
                description="Eyewitness account by a bishop who attended the council."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="Isidore of Seville's History of the Goths",
                author_role="bishop-historian",
                year=625,
                place="Seville",
                extant=True,
                transmission=[
                    TransmissionStep(via="Acts of Toledo (extant)", year=589, type="summary"),
                    TransmissionStep(via="John of Biclar (extant)", year=590, type="summary")
                ],
                description="Isidore synthesizes OTHER EXTANT accounts 35 years later (Acts and John's Chronicle)."
            ),
        ],
        edges=[
            Edge(from_id="evt_conversion_589", to="n1", kind="official_record"),
            Edge(from_id="evt_conversion_589", to="n2", kind="eyewitness"),
            Edge(from_id="n1", to="n3", kind="synthesis"),
            Edge(from_id="n2", to="n3", kind="synthesis"),
        ],
        topics=[
            Topic(id="t_event", label="The conversion (589 CE)", anchor="evt_conversion_589"),
            Topic(id="t_isidore", label="Isidore of Seville's historiography (early 7th c.)", anchor="n3"),
        ]
    )


def generate_battle_of_tours() -> Scenario:
    """Scenario 8: Battle of Tours (732 CE) - Hard."""
    return Scenario(
        id="scenario_8_tours",
        difficulty="hard",
        event=Event(
            id="evt_tours_732",
            title="Battle of Tours (Charles Martel vs. Umayyad forces)",
            year=732,
            place="Near Tours, Francia",
            description="Charles Martel defeats Umayyad army, halting Muslim expansion into Francia.",
            image_url=None,  # Image temporarily disabled
            composition_info="The Mozarabic Chronicle (754) from Muslim Iberia and the Continuations of Fredegar (760) from Francia provide near-contemporary but regionally partisan perspectives. The Continuations compiled lost Frankish court records. 19th-century French nationalist historians transformed a frontier skirmish into a civilizational showdown."
        ),
        nodes=[
            SourceNode(
                id="n1",
                type="text",
                title="Mozarabic Chronicle of 754",
                author_role="Iberian Christian chronicler",
                year=754,
                place="Al-Andalus",
                extant=True,
                description="Written 22 years after the battle from the Muslim-ruled Iberian perspective."
            ),
            SourceNode(
                id="lost_court",
                type="text",
                title="Lost Frankish Court Records of the Battle",
                author_role="court scribe",
                year=735,
                place="Francia",
                extant=False,
                description="Lost official court records documenting Charles Martel's victory over the Umayyad forces. These records no longer survive but were compiled into the Continuations of Fredegar."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Continuations of Fredegar",
                author_role="Frankish annalist",
                year=760,
                place="Francia",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: Frankish court records", year=735, type="compilation")
                ],
                description="Frankish chronicle compiled ~30 years later from lost court records that no longer survive."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="19th-century French nationalist history",
                author_role="modern nationalist historian",
                year=1850,
                place="Paris",
                extant=True,
                transmission=[
                    TransmissionStep(via="Continuations of Fredegar (extant)", year=760, type="summary")
                ],
                description="19th-century work analyzing OTHER EXTANT sources (the Continuations) to glorify the battle."
            ),
        ],
        edges=[
            Edge(from_id="evt_tours_732", to="n1", kind="near_contemporary"),
            Edge(from_id="evt_tours_732", to="lost_court", kind="lost_court_record"),
            Edge(from_id="lost_court", to="n2", kind="compilation"),
            Edge(from_id="n2", to="n3", kind="nationalist_interpretation"),
        ],
        topics=[
            Topic(id="t_event", label="The battle itself (732 CE)", anchor="evt_tours_732"),
            Topic(id="t_nationalism", label="19th-century French nationalism", anchor="n3"),
        ]
    )


def generate_gregory_of_tours() -> Scenario:
    """Scenario 9: Gregory of Tours writing his Histories (590s CE) - Medium."""
    return Scenario(
        id="scenario_9_gregory",
        difficulty="medium",
        event=Event(
            id="evt_gregory_writing_590",
            title="Gregory of Tours completes his 'Histories'",
            year=594,
            place="Tours, Francia",
            description="Bishop Gregory finishes his ten-book history of the Franks.",
            image_url=None,  # Image temporarily disabled
            composition_info="Gregory's original manuscript disappeared within a century; our text depends entirely on Carolingian manuscript copies made 200+ years later from the lost autograph. The 1951 critical edition analyzes these surviving medieval copies."
        ),
        nodes=[
            SourceNode(
                id="lost_autograph",
                type="text",
                title="Gregory's Lost Autograph Manuscript",
                author_role="bishop-historian (author)",
                year=594,
                place="Tours",
                extant=False,
                description="Lost original manuscript written in Gregory of Tours' own hand. The autograph no longer survives; our text depends entirely on later medieval copies."
            ),
            SourceNode(
                id="n1",
                type="text",
                title="Carolingian manuscript copy",
                author_role="Carolingian scribe",
                year=820,
                place="Corbie Abbey",
                extant=True,
                transmission=[
                    TransmissionStep(via="lost: Gregory's autograph manuscript", year=594, type="copy")
                ],
                description="Earliest surviving manuscript, copied 220 years after Gregory wrote from his now-lost original."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Modern critical edition (1951)",
                author_role="modern philologist",
                year=1951,
                place="France",
                extant=True,
                transmission=[
                    TransmissionStep(via="Carolingian manuscripts (extant)", year=820, type="summary")
                ],
                description="Scholarly edition analyzing OTHER EXTANT medieval manuscripts to reconstruct the text."
            ),
        ],
        edges=[
            Edge(from_id="evt_gregory_writing_590", to="lost_autograph", kind="authorship"),
            Edge(from_id="lost_autograph", to="n1", kind="manuscript_copy"),
            Edge(from_id="n1", to="n2", kind="scholarly_edition"),
        ],
        topics=[
            Topic(id="t_authorship", label="Gregory's authorship (594 CE)", anchor="evt_gregory_writing_590"),
            Topic(id="t_transmission", label="Carolingian manuscript culture (9th c.)", anchor="n1"),
        ]
    )


def generate_byzantine_embassy() -> Scenario:
    """Scenario 10: Byzantine embassy to the West (580 CE) - Easy."""
    return Scenario(
        id="scenario_10_embassy",
        difficulty="easy",
        event=Event(
            id="evt_embassy_580",
            title="Byzantine embassy to Merovingian Francia",
            year=580,
            place="Gaul",
            description="Emperor Tiberius II sends envoys to negotiate with the Franks.",
            image_url=None,  # Image temporarily disabled
            composition_info="Gregory of Tours casually mentions the embassy in his Histories (584), providing our only surviving narrative; Byzantine court records are entirely lost. A later Merovingian chronicle summarizes Gregory's account, and a modern historian analyzes both."
        ),
        nodes=[
            SourceNode(
                id="lost_byzantine",
                type="text",
                title="Lost Byzantine Court Records",
                author_role="imperial secretary",
                year=580,
                place="Constantinople",
                extant=False,
                description="Lost official Byzantine court records documenting the embassy sent to the Merovingian Franks. These imperial records no longer survive; we depend entirely on Western sources."
            ),
            SourceNode(
                id="n1",
                type="text",
                title="Gregory of Tours' mention in Book VI",
                author_role="bishop (contemporary)",
                year=584,
                place="Tours",
                extant=True,
                description="Gregory mentions the embassy in passing, as a near-contemporary observer just 4 years later."
            ),
            SourceNode(
                id="n2",
                type="text",
                title="Fredegar's Chronicle",
                author_role="Frankish chronicler",
                year=660,
                place="Francia",
                extant=True,
                transmission=[
                    TransmissionStep(via="Gregory of Tours (extant)", year=584, type="summary")
                ],
                description="7th-century chronicle summarizing Gregory's account and adding Frankish perspective."
            ),
            SourceNode(
                id="n3",
                type="text",
                title="Modern study of Byzantine-Frankish relations",
                author_role="modern historian",
                year=2015,
                place="University",
                extant=True,
                transmission=[
                    TransmissionStep(via="Gregory (extant)", year=584, type="summary"),
                    TransmissionStep(via="Fredegar (extant)", year=660, type="summary")
                ],
                description="Modern historical analysis of OTHER EXTANT sources (Gregory and Fredegar)."
            ),
        ],
        edges=[
            Edge(from_id="evt_embassy_580", to="n1", kind="near_contemporary_witness"),
            Edge(from_id="evt_embassy_580", to="lost_byzantine", kind="official_record_lost"),
            Edge(from_id="n1", to="n2", kind="derivative"),
            Edge(from_id="n1", to="n3", kind="modern_analysis"),
            Edge(from_id="n2", to="n3", kind="modern_analysis"),
        ],
        topics=[
            Topic(id="t_event", label="The embassy itself (580 CE)", anchor="evt_embassy_580"),
        ]
    )
