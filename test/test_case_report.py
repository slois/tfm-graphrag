from src.rag import DiMonarchKG

cases = [
        {
            'id': 'C01',
            'case_report': """A pediatric patient presented with moderate intellectual disability, global developmental 
            delay, and microcephaly. The neonatal history was notable for a characteristic high-pitched, cat-like cry. 
            Physical examination revealed facial dysmorphism including hypertelorism and micrognathia.""",
            'mondo_id': 'MONDO:0007404',
            'disease_name': 'Cri-du-chat syndrome',
            'causal_genes': [],
            'doi': 'https://doi.org/10.1186/s13256-020-02590-8'
        },
        {
            'id': 'C02',
            'case_report': """The 8-year-old Colombian girl is the first child born at term to 27-year-old nonconsanguineous parents after prolonged labor and perinatal hypoxia, with an Apgar score of 6 at 10 min. The child was admitted to the neonatal intensive care unit requiring mechanical ventilation for 27 days. Clinical follow-up showed hypotonia and DD (head control at 7 months, sitting at 12 months, standing at 24 months, walking at 28 months, and currently speaking only 2 words) with dysmorphic features including midfacial hypoplasia, hypertelorism, micrognathia, epicanthic fold, prominent teeth, upslanting palpebral fissures (Fig. 1), and laryngomalacia requiring 8 surgical interventions due to glottal stenosis. Her family history was unremarkable Brain MRI revealed frontal and temporal cortical atrophy with loss of posterior ventricular white matter.""",
            'mondo_id': "MONDO:0014358",
            'disease_name': "Xia-Gibbs syndrome",
            'causal_genes': ['AHDC1'],
            'doi': 'https://doi.org/10.1159/000479357'
        },
        {
            'id': 'C03',
            'case_report': """"A 1,840 g male was delivered via normal vaginal delivery in our hospital at 32 weeks gestational age at May 2009. His mother was 40-yr-old, and had gestational diabetes mellitus and polyhydramnios. Apgar scores were 2 and 4 at 1 and 5 min, respectively. The patient presented with cyanosis and respiratory difficulty requiring continuous positive airway pressure. No evidence of respiratory distress syndrome was noted on a chest radiograph. A laryngeal anomaly and large tongue base were evident, which nearly obstructed the vocal cord. A physical examination revealed bushy eyebrows and synophrys, long curly eyelashes, long philtrum, downturned angles of the mouth and thin upper lips, cleft palate, micrognathia, excessive body hair, micromelia of both hands, flexion contracture of elbows and hypertonicity. A brain sonogram revealed increased periventricular echogenicity. Computed tomography (CT) of the neck revealed no abnormality in upper airway except micrognathia. However, the patient had suffered from upper airway obstruction due to secretion from 1 month of age, which led to tracheostomy at 3 months of age. The patient exhibited feeding intolerance. Abdominal ultrasonography and upper GI series showed gastroesophageal reflux but no other abnormalities. Chromosome analysis showed a normal karyotype, 46, XY. The parents rejected their gene analysis. The patient had been hospitalized for 5 months due to recurrent sepsis and respiratory problems. At 5 months of age, the patient was discharged and did not visit for 5 months after discharge.""",
            'mondo_id': 'MONDO:0016033',
            'disease_name': 'Cornelia de Lange syndrome with NIPBL mutation',
            'causal_genes': ['NIPBL'],
            'doi': 'https://doi.org/10.1002/ccr3.1010'
        },
        {
            'id': 'C04',
            'case_report': """A 7‐month‐old female infant was referred to genetics clinic for an evaluation of microcephaly, failure to thrive (FTT), and dysmorphic features. The patient was born at 38 weeks gestation to a 21‐year‐old mother with no history of prior pregnancy who had a history of nausea and preeclampsia throughout the pregnancy. She was delivered via cesarean section with Apgar scores of 8 and 9 after 1 and 5 min respectively. Birthweight (BW) was 2.24 kg, birth length was 47 cm. The patient was admitted to the Neonatal Intensive Care Unit for 1 week due to hypothermia, feeding issues, and jaundice which resolved without phototherapy. The patient received feeds via a nasogastric tube for 1 week after birth, then was discharged home, and followed by her pediatrician.
    On evaluation, the patient's weight was 5.89 kg (1st %), length was 62 cm (<1st %), and occipitofrontal head circumference (OFC) was 40.5 cm (2.8th %). The patient had microcephaly with bitemporal narrowing of the forehead, hirsutism, arched thick eyebrows, synophrys, bilateral epicanthal folds, long curly eyelashes, and mild ptosis. Her nose appeared short and upturned, with a flat nasal bridge. She also had a small oral cavity, high‐arched palate, and a small chin with mild retrognathia. Her limb examination showed proximally placed thumbs, bilateral fifth finger clinodactyly, small 4th and 5th metacarpals, and mild 2nd and 3rd toes syndactyly.
    Her neurological examination showed low generalized muscle bulk and hypotonia. There was no evidence of tremors or abnormal movements, and deep tendon reflexes were within normal limits. Developmentally, she sat independently at 7 months.
    On follow‐up examination at the age of 14 months, she was noted to have improved oral intake after feeding therapy. Her weight increased to 8.2 kg (10%), length measured 74 cm (15%), but OFC remained relatively small at 43 cm (5%). A developmental assessment carried out at that age showed she was advanced in her fine motor skills at 21 months of age, but gross motor skills were delayed at 11 months of age, and expressive language was at 12 months of age. She was able to pull herself up to stand and walked with support while leaning on the furniture. She began to walk independently by age 15 months.
    Because the patient was not babbling, she was receiving speech therapy through early intervention. Echocardiogram identified a trivial patent foramen oval, with a mild atrial left to right shunt. Renal ultrasound was normal.
    """,
            'mondo_id': 'MONDO:0012555',
            'disease_name': 'Cornelia de Lange Syndrome due to novel duplication in SMC3',
            'causal_genes': ['SMC3'],
            'doi': 'https://doi.org/10.1002/ccr3.1010'
        },
        {
            'id': 'C05',
            'case_report': """The proband (younger brother) in this family had microcephaly (−4 SD), and dysmorphic features including mild hypertelorism, downturned mouth, coarse facial features, in addition to cryptorchidism, and micropenis. His brother was also dysmorphic with coarse facial features, microcephaly, ambiguous genitalia, and coarctation of the aorta in conjunction with a bicuspid aortic valve. Both brothers had severe intellectual disability (non-verbal) and mild microcytic anemia. The mother is phenotypically normal. A three-generation family history was queried and there was no history of cancer in the family. Both parents are of Armenian descent and consanguinity was denied. 
            Pathology review revealed an epithelioid osteosarcoma, primarily composed of cells with oval eccentric nuclei and voluminous lightly eosinophilic cytoplasm.""",
            'mondo_id': 'MONDO:0016980',
            'disease_name': "ATR-X-related syndrome and osteosarcoma",
            'causal_genes': ['ATRX'],
            'doi': 'https://doi.org/10.1002/ajmg.a.38184'
        },
        {
            'id': 'C06',
            'case_report': """A 6-year-old boy referred for moderate developmental delay and facial dysmorphic features. Examination: arched eyebrows with sparse outer third, long and abundant eyelashes, depressed nasal tip, large ears with prominent helix, persistence of fetal pads on the fingertips. Short stature (3rd percentile). Treated congenital heart disease (ventricular septal defect). No history of seizures. Sociable behavior with an interest in music""",
            'mondo_id': 'MONDO:0016512',
            'disease_name': 'Síndrome de Kabuki tipo 1',
            'causal_genes': ['KMT2D'],
            'doi': 'https://doi.org/10.1016/s0022-3476(81)80255-7'
        },
        {
            'id': 'C07',
            'case_report': """A 3-year-old girl with severe psychomotor delay, complete absence of verbal language, and characteristic behavior: frequent, easy laughter, fascination with water, motor hyperactivity, and affectionate behavior. Ataxic gait with tremor of the extremities. Dysmorphic features: microcephaly, relative hypopigmentation of the skin compared to her parents, prognathism, and macrostomia. Epileptic seizures that are difficult to control: atypical absences and myoclonic seizures with an EEG pattern of high-amplitude delta waves peaking in anterior regions. Brain MRI: mild hypomyelination.""",
            'mondo_id': 'MONDO:0008902',
            'disease_name': 'Angelman syndrome',
            'causal_genes': ['UBE3A'],
            'doi': 'https://doi.org/10.1111/j.1469-8749.1965.tb07844.x'
        },
        {
            'id': 'C08',
            'case_report': """A 5-year-old boy with severe global developmental delay, absence of functional language (communication via pictograms), behavior with features of the autism spectrum (lack of eye contact, repetitive hand movements, sensory hypersensitivity), and generalized hypotonia. Dysmorphic features: dolichocephaly, large ears, long philtrum, large hands with a conical fifth finger. Epileptic seizures beginning at age 3 (epileptic spasms in bursts), with partial response to vigabatrin. Brain MRI: corpus callosum hypoplasia and mild ventricular dilation.""",
            'mondo_id': 'MONDO:0015749',
            'disease_name': 'Phelan-McDermid syndrome',
            'causal_genes': ['SHANK3'],
            'doi': 'https://doi.org/10.1159/000334260'
        },
        {
            'id': 'C09',
            'case_report': """A 4-year-old girl with moderate-to-severe global developmental delay, absence of functional language, and cheerful behavior with sustained eye contact. Physical examination: mild microcephaly, short philtrum, low-set ears, and bilateral clinodactyly of the fifth finger. No documented epileptic seizures. Normal brain MRI.""",
            'mondo_id': 'MONDO:0012827',
            'disease_name': 'Mowat-Wilson syndrome',
            'causal_genes': ['ZEB2'],
            'doi': 'https://doi.org/10.1136/jmg.40.5.305'
        },
        {
            'id': 'C10',
            'case_report': """Both individuals presented with the well-known characteristic features, as well as rarer anomalies seen in a minority of patients. Patient 1 presented shortly after birth with an enlarged cisterna magna, distal contractures, and distinctive facies that included bitemporal narrowing and deep set eyes. Patient 2 presented at 7 months of age with microcephaly and dysmorphic features. These individuals, and the 52 cases reviewed from the literature, show characteristic features including global developmental delay, ID, microcephaly, feeding difficulties, and the facial gestalt. Other common findings include seizures, vision defects, brain abnormalities and skeletal abnormalities of the hands and feet. Less common features include optic nerve defects, contractures, ataxia, and cardiac anomalies.""",
            'mondo_id': 'MONDO:0000508',
            'disease_name': 'syndromic intellectual disability',
            'causal_genes': ['DYRK1A'],
            'doi': 'https://doi.org/10.1186/s12881-016-0276-4'
        },
        {
            'id': 'C11',
            'case_report': """A 9-year-old boy with mild-to-moderate intellectual disability and specific learning difficulties. Normal motor development (walking at 13 months). No history of seizures. No dysmorphic facial features. Physical examination is unremarkable. Brain MRI is normal. Family history reveals a maternal uncle with similar cognitive impairment. Social behavior is appropriate for age.""",
            'mondo_id': 'MONDO:0015286',
            'disease_name': 'X-linked intellectual disability, nonsyndromic',
            'causal_genes': ['AP1S2'],
            'doi': 'synthetic'
        },
        {
            'id': 'C12',
            'case_report': """A 4-year-old girl with global developmental delay and epilepsy starting at 6 months of age. Seizure types include focal seizures with impaired awareness and occasional generalized tonic-clonic seizures. EEG shows multifocal epileptiform discharges. No dysmorphic features are noted. Growth parameters are normal. Brain MRI is unremarkable. Language development is severely impaired.""",
            'mondo_id': 'MONDO:0100030',
            'disease_name': 'Developmental and epileptic encephalopathy',
            'causal_genes': ['STXBP1'],
            'doi': 'synthetic'
        },
        {
            'id': 'C13',
            'case_report': """A 6-year-old boy with moderate intellectual disability and epilepsy since age 2 (generalized tonic and atonic seizures). Facial features include broad nasal bridge, mild hypertelorism, and low-set ears. No major congenital anomalies are identified. Brain MRI is normal. Growth parameters are within normal limits.""",
            'mondo_id': 'MONDO:0000000',
            'disease_name': 'Syndromic intellectual disability with epilepsy',
            'causal_genes': ['SYNGAP1'],
            'doi': 'synthetic'
        },
        {
            'id': 'C14',
            'case_report': """A 5-year-old girl with mild developmental delay, especially affecting language. No seizures. Subtle facial features including slightly upslanting palpebral fissures and a thin upper lip, considered within normal variation by previous evaluations. Normal growth. Behavioral profile shows mild social anxiety. Brain MRI is normal.""",
            'mondo_id': 'MONDO:0000000',
            'disease_name': 'Uncertain syndromic vs nonsyndromic intellectual disability',
            'causal_genes': [],
            'doi': 'synthetic'
        }
    ]

if __name__ == '__main__':

    model = DiMonarchKG()

    query_template = """
    Case report:
    {case_report}
    
    - Which disease are most likely to be related with these phenotypes and which genes are associated to them?
    """

    for case in cases[13:14]:
        query_text = query_template.format(case_report=case['case_report'])
        print(f"--- USER ---\n{query_text}")

        answer = model.search(query_text=query_text, return_context=True)

        if answer is not None:
            print(f"\n--- ANSWER ---\n"
                  f"{answer.answer}\n")

            print(f"\n--- TOOLS RETRIEVER ---\n"
                  f"{answer.retriever_result.metadata['tools_selected']}")