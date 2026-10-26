# Manual journal classification: tier (C=core LIS, A=adjacent, P=peripheral) and domain.
# Coding rule: the journal's stated scope and disciplinary tradition, not its current topical mix.
# Validated afterwards against a data-driven lexical LIS-centrality score.
LIB, INF, SCI, ARC = "Librarianship", "Information science & KO", "Scientometrics & scholarly comm.", "Archives & records"
ISM, COM, HER = "Information systems & KM", "Communication & information society", "Book, heritage & digital humanities"
CMP, NAT, OSS = "Computing & data science", "Natural & health sciences", "Other social sciences & humanities"

RAW = """
f1000research|P|NAT
journal of chemical information and modeling|P|NAT
scientific data|P|NAT
education and information technologies|P|OSS
library philosophy and practice|C|LIB
ieee transactions on information theory|P|CMP
scientometrics|C|SCI
information processing and management|C|INF
information studies: theory and application|C|INF
library and information service|C|LIB
kybernetes|P|CMP
journal of modern information|C|INF
proceedings of the association for information science and technology|C|INF
data analysis and knowledge discovery|C|INF
information communication and society|A|COM
information sciences letters|P|CMP
profesional de la informacion|A|COM
notes and queries|P|OSS
international journal of information management|A|ISM
journal of academic librarianship|C|LIB
personal and ubiquitous computing|P|CMP
journal of cheminformatics|P|NAT
journal of the association for information science and technology|C|INF
international journal of geographical information science|P|CMP
information technology and people|A|ISM
big data and society|A|COM
telecommunications policy|P|OSS
journal of library and information science in agriculture|C|LIB
journal of statistics applications and probability|P|CMP
journal of documentation|C|INF
journal of informetrics|C|SCI
college and research libraries news|C|LIB
journal of health communication|P|NAT
development and learning in organizations|P|OSS
documentation, information and knowledge|C|INF
library hi tech|C|LIB
journal of information science|C|INF
journal of information and knowledge management|A|ISM
information systems research|A|ISM
journal of information science and engineering|P|CMP
social science computer review|A|COM
online information review|C|INF
webology|C|INF
bibliotekarz podlaski|C|LIB
government information quarterly|A|ISM
journal of enterprise information management|A|ISM
journal of librarianship and information science|C|LIB
frontiers in research metrics and analytics|C|SCI
learned publishing|C|SCI
journal of library administration|C|LIB
quantitative science studies|C|SCI
journal of the medical library association|C|LIB
digital humanities quarterly|A|HER
ethics and information technology|A|COM
publishing and printing|A|HER
revista cubana de informacion en ciencias de la salud|C|INF
knowledge management research and practice|A|ISM
journal of scientometric research|C|SCI
international journal of information management data insights|A|ISM
acervo|C|ARC
college and research libraries|C|LIB
evidence based library and information practice|C|LIB
global knowledge, memory and communication|C|INF
international journal of information science and management|C|INF
information research|C|INF
aslib journal of information management|C|INF
journal of decision systems|P|CMP
library hi tech news|C|LIB
encontros bibli|C|INF
ciencia da informacao|C|INF
publications|C|SCI
desidoc journal of library and information technology|C|LIB
journal of library science in china|C|LIB
information development|C|INF
technical services quarterly|C|LIB
language resources and evaluation|P|CMP
journal of payavard salamat|P|NAT
vine journal of information and knowledge management systems|A|ISM
revista ibero-americana de ciencia da informacao|C|INF
data intelligence|P|CMP
tuna|A|HER
serials librarian|C|LIB
electronic library|C|LIB
ifla journal|C|LIB
vjesnik bibliotekara hrvatske|C|LIB
portal|C|LIB
european journal of information systems|A|ISM
research evaluation|C|SCI
accountability in research|A|COM
gazette des archives|C|ARC
information and learning science|A|COM
library management|C|LIB
cuadernos.info|A|COM
cataloging and classification quarterly|C|INF
bibliotecas, anales de investigacion|C|LIB
health information and libraries journal|C|LIB
knowledge organization|C|INF
journal of indian library association|C|LIB
information-wissenschaft und praxis|C|INF
jlis.it|C|LIB
desde el sur|P|OSS
zeitschrift fur bibliothekswesen und bibliographie|C|LIB
investigacion bibliotecologica|C|LIB
information services and use|C|INF
digital library perspectives|C|LIB
world patent information|A|ISM
international journal of media and information literacy|A|COM
manuscript and book heritage of ukraine|A|HER
interacting with computers|P|CMP
canadian journal of program evaluation|P|OSS
library and information science research|C|LIB
data technologies and applications|A|ISM
journal of hospital librarianship|C|LIB
library trends|C|LIB
global intellectual history|P|OSS
information technology and libraries|C|LIB
revista digital de biblioteconomia e ciencia da informacao|C|INF
medical reference services quarterly|C|LIB
atoz|C|INF
open praxis|P|OSS
language documentation and conservation|P|OSS
public library quarterly|C|LIB
international journal of multimedia information retrieval|P|CMP
journal of electronic resources librarianship|C|LIB
indexer|C|INF
journal of classification|P|CMP
indian journal of information sources and services|C|INF
scires-it|A|HER
international information and library review|C|LIB
bulletin des bibliotheques de france|C|LIB
bibliothecae.it|C|LIB
journal of the australian library and information association|C|LIB
information discovery and delivery|C|INF
perspectivas em ciencia da informacao|C|INF
serials review|C|LIB
annals of library and information studies|C|LIB
reference services review|C|LIB
aib studi|C|LIB
journal of data and information science|C|SCI
revista espanola de documentacion cientifica|C|INF
international journal on digital libraries|C|LIB
public services quarterly|C|LIB
archival science|C|ARC
social science information|P|OSS
information systems management|A|ISM
knowledge cultures|P|OSS
tekst, kniga, knigoizdaniye|A|HER
transinformacao|C|INF
anuario electronico de estudios en comunicacion social disertaciones|A|COM
record and library journal|C|LIB
libri|C|LIB
education for information|C|INF
latvijas nacionalas bibliotekas zinatniskie raksti|C|LIB
revista general de informacion y documentacion|C|INF
library quarterly|C|LIB
journal of information technology|A|ISM
journal of education for library and information science|C|LIB
science and technology libraries|C|LIB
z badan nad ksiazka i ksiegozbiorami historycznymi|A|HER
journal of information science theory and practice|C|INF
bid|C|LIB
moderna arhivistika|C|ARC
umanistica digitale|A|HER
journal of information and organizational sciences|A|ISM
wacana|P|OSS
comma|C|ARC
journal of information technology teaching cases|A|ISM
journal of information literacy|C|LIB
american archivist|C|ARC
data and information management|C|INF
knygotyra|A|HER
scientometrics research journal|C|SCI
fukushima journal of medical sciences|P|NAT
journal of open humanities data|A|HER
voeb-mitteilungen|C|LIB
manuscript studies|A|HER
ic revista cientifica de informacion y comunicacion|A|COM
acta informatica pragensia|A|ISM
insights: the uksg journal|C|LIB
collection management|C|LIB
new review of academic librarianship|C|LIB
international journal of information, diversity and inclusion|C|LIB
international journal of data mining and bioinformatics|P|CMP
informacion, cultura y sociedad|C|LIB
slavic and east european information resources|C|LIB
notes|C|LIB
library|A|HER
journal of open research software|P|CMP
przeglad archiwalny instytutu pamieci narodowej|C|ARC
methis|P|OSS
fontes artis musicae|C|LIB
malaysian journal of library and information science|C|LIB
proceedings from the document academy|C|INF
computers in the schools|P|OSS
manuscripta orientalia|A|HER
international journal of knowledge processing studies|A|ISM
information resources management journal|A|ISM
library resources and technical services|C|LIB
science editor and publisher|A|HER
journal of business and finance librarianship|C|LIB
information and organization|A|ISM
art documentation|C|LIB
preservation, digital technology and culture|C|LIB
revista interamericana de bibliotecologia|C|LIB
international journal of law and information technology|P|OSS
ibersid|C|INF
logos|A|HER
iberoamerican journal of science measurement and communication|C|SCI
transactions of the international society for music information retrieval|P|CMP
collection and curation|C|LIB
archives and manuscripts|C|ARC
records management journal|C|ARC
comparative oriental manuscript studies bulletin|A|HER
journal of librarianship and scholarly communication|C|SCI
library leadership and management|C|LIB
open information science|C|INF
internet reference services quarterly|C|LIB
archiwa, biblioteki i muzea koscielne|C|ARC
grey journal|C|INF
boletim do arquivo da universidade de coimbra|A|HER
african journal of library archives and information science|C|LIB
biblios|C|LIB
journal of library and information services in distance learning|C|LIB
papers of the bibliographical society of america|A|HER
book history|A|HER
journal of access services|C|LIB
college and undergraduate libraries|C|LIB
international journal of legal information|C|LIB
communications in information literacy|C|LIB
bottom line|C|LIB
issues in science and technology librarianship|C|LIB
journal of electronic resources in medical libraries|C|LIB
international journal of metadata, semantics and ontologies|A|ISM
bulletin of the john rylands library|A|HER
journal of library and information studies|C|LIB
quaerendo|A|HER
information retrieval journal|A|ISM
vjesnik dalmatinskih arhiva|C|ARC
information and culture|C|INF
journal of map and geography libraries|C|LIB
atlanti+|C|ARC
legal reference services quarterly|C|LIB
palabra clave (la plata)|C|LIB
journal of codicology and manuscript research|A|HER
ip indian journal of library science and information technology|C|LIB
law library journal|C|LIB
information design journal|A|COM
digital transformation and society|A|ISM
journal of educational media and library sciences|C|LIB
bilgi dunyasi|C|LIB
music reference services quarterly|C|LIB
archivaria|C|ARC
liber quarterly|C|LIB
journal of the canadian health libraries association|C|LIB
reference librarian|C|LIB
iafor journal of literature and librarianship|C|LIB
arhivski vjesnik|C|ARC
journal of learning spaces|A|COM
scire|C|INF
archeion|C|ARC
information and media|A|COM
performance measurement and metrics|C|LIB
informing science|A|ISM
terminology|P|OSS
discover computing|A|ISM
masaryk university journal of law and technology|P|OSS
journal of information ethics|A|COM
teorie vedy / theory of science|P|OSS
scriptorium|A|HER
journal of library metadata|C|LIB
revista de cancioneros impresos y manuscritos|A|HER
folia toruniensia|C|LIB
journal of web librarianship|C|LIB
international journal of technology, knowledge and society|P|OSS
bibliotecas|C|LIB
knihy a dejiny|A|HER
script and print|A|HER
archives|C|ARC
libres|C|LIB
polish libraries|C|LIB
journal of archival organization|C|ARC
east asian publishing and society|A|HER
international journal of public administration in the digital age|A|ISM
pakistan journal of information management and libraries|C|LIB
library progress international|C|LIB
canadian journal of information and library science|C|LIB
school library research|C|LIB
scholarly assessment reports|C|SCI
information, medium, and society|A|COM
reference and user services quarterly|C|LIB
transactions of the cambridge bibliographical society|A|HER
library and information science|C|LIB
in monte artium|A|HER
journal of interlibrary loan, document delivery and electronic reserve|C|LIB
anales de documentacion|C|INF
"""
D = {"LIB": LIB, "INF": INF, "SCI": SCI, "ARC": ARC, "ISM": ISM, "COM": COM, "HER": HER, "CMP": CMP, "NAT": NAT, "OSS": OSS}
TIERS = {}
for line in RAW.strip().splitlines():
    n, t, d = line.split("|")
    TIERS[n] = (t, D[d])

import re
RENAMED = {"library review": "global knowledge, memory and communication", "program": "data technologies and applications",
           "bulletin of the john rylands university library of manchester": "bulletin of the john rylands library", "collection building": "collection and curation",
           "australian academic and research libraries": "journal of the australian library and information association", "information retrieval": "information retrieval journal",
           "school library media research": "school library research", "journal of educational media and library science": "journal of educational media and library sciences"}
def norm(s):
    s = s.strip().lower()
    s = RENAMED.get(re.sub(r"\s+", " ", s), s)
    s = re.sub(r"\s*:\s*jmla$", "", s)
    s = re.sub(r"\s*\((the )?netherlands\)$", "", s)
    s = re.sub(r"journal of medical science$", "journal of medical sciences", s)
    return re.sub(r"\s+", " ", s)
