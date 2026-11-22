import streamlit as st, yfinance as yf, pandas as pd, numpy as np, warnings
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss
warnings.filterwarnings("ignore")
st.set_page_config(page_title="NexTrade Entry & Exit Lab", page_icon="📈", layout="wide")
WATCH={
    "360ONE — 360ONE":"360ONE.NS",
    "3MINDIA — 3MINDIA":"3MINDIA.NS",
    "5PAISA — 5PAISA":"5PAISA.NS",
    "AARTIDRUGS — AARTIDRUGS":"AARTIDRUGS.NS",
    "AARTIIND — AARTIIND":"AARTIIND.NS",
    "AARTISURF — AARTISURF":"AARTISURF.NS",
    "AAVAS — AAVAS":"AAVAS.NS",
    "ABB — ABB":"ABB.NS",
    "ABBOTINDIA — ABBOTINDIA":"ABBOTINDIA.NS",
    "ABCAPITAL — ABCAPITAL":"ABCAPITAL.NS",
    "ABFRL — ABFRL":"ABFRL.NS",
    "ACC — ACC":"ACC.NS",
    "ADANIENSOL — ADANIENSOL":"ADANIENSOL.NS",
    "ADANIENT — ADANIENT":"ADANIENT.NS",
    "ADANIGREEN — ADANIGREEN":"ADANIGREEN.NS",
    "ADANIPORTS — ADANIPORTS":"ADANIPORTS.NS",
    "ADANIPOWER — ADANIPOWER":"ADANIPOWER.NS",
    "ADSL — ADSL":"ADSL.NS",
    "AEGISCHEM — AEGISCHEM":"AEGISCHEM.NS",
    "AFFLE — AFFLE":"AFFLE.NS",
    "AGARIND — AGARIND":"AGARIND.NS",
    "AHLUCONT — AHLUCONT":"AHLUCONT.NS",
    "ALANKIT — ALANKIT":"ALANKIT.NS",
    "ALKEM — ALKEM":"ALKEM.NS",
    "ALLCARGO — ALLCARGO":"ALLCARGO.NS",
    "ALMONDZ — ALMONDZ":"ALMONDZ.NS",
    "AMARAJABAT — AMARAJABAT":"AMARAJABAT.NS",
    "AMBER — AMBER":"AMBER.NS",
    "AMBUJACEM — AMBUJACEM":"AMBUJACEM.NS",
    "AMIORG — AMIORG":"AMIORG.NS",
    "ANANTRAJ — ANANTRAJ":"ANANTRAJ.NS",
    "ANDHRAPAP — ANDHRAPAP":"ANDHRAPAP.NS",
    "ANGELONE — ANGELONE":"ANGELONE.NS",
    "ANURAS — ANURAS":"ANURAS.NS",
    "APARINDS — APARINDS":"APARINDS.NS",
    "APEX — APEX":"APEX.NS",
    "APLAPOLLO — APLAPOLLO":"APLAPOLLO.NS",
    "APOLLOHOSP — APOLLOHOSP":"APOLLOHOSP.NS",
    "APOLLOPIPE — APOLLOPIPE":"APOLLOPIPE.NS",
    "APOLLOTYRE — APOLLOTYRE":"APOLLOTYRE.NS",
    "APTUS — APTUS":"APTUS.NS",
    "ARE&M — ARE&M":"ARE&M.NS",
    "ARVINDFASN — ARVINDFASN":"ARVINDFASN.NS",
    "ASAHIINDIA — ASAHIINDIA":"ASAHIINDIA.NS",
    "ASALCBR — ASALCBR":"ASALCBR.NS",
    "ASHAPURMIN — ASHAPURMIN":"ASHAPURMIN.NS",
    "ASHOKA — ASHOKA":"ASHOKA.NS",
    "ASHOKLEY — ASHOKLEY":"ASHOKLEY.NS",
    "ASIANPAINT — ASIANPAINT":"ASIANPAINT.NS",
    "ASTEC — ASTEC":"ASTEC.NS",
    "ASTERDM — ASTERDM":"ASTERDM.NS",
    "ASTRAL — ASTRAL":"ASTRAL.NS",
    "ATAM — ATAM":"ATAM.NS",
    "ATGL — ATGL":"ATGL.NS",
    "ATUL — ATUL":"ATUL.NS",
    "AUBANK — AUBANK":"AUBANK.NS",
    "AURIONPRO — AURIONPRO":"AURIONPRO.NS",
    "AUROPHARMA — AUROPHARMA":"AUROPHARMA.NS",
    "AUTOAXLES — AUTOAXLES":"AUTOAXLES.NS",
    "AVALON — AVALON":"AVALON.NS",
    "AVANTIFEED — AVANTIFEED":"AVANTIFEED.NS",
    "AXISBANK — AXISBANK":"AXISBANK.NS",
    "AXISCADES — AXISCADES":"AXISCADES.NS",
    "BAJAJ-AUTO — BAJAJ-AUTO":"BAJAJ-AUTO.NS",
    "BAJAJFINSV — BAJAJFINSV":"BAJAJFINSV.NS",
    "BAJAJHFL — BAJAJHFL":"BAJAJHFL.NS",
    "BAJAJHLDNG — BAJAJHLDNG":"BAJAJHLDNG.NS",
    "BAJFINANCE — BAJFINANCE":"BAJFINANCE.NS",
    "BALAMINES — BALAMINES":"BALAMINES.NS",
    "BALKRISIND — BALKRISIND":"BALKRISIND.NS",
    "BALRAMCHIN — BALRAMCHIN":"BALRAMCHIN.NS",
    "BANDHANBNK — BANDHANBNK":"BANDHANBNK.NS",
    "BANKBARODA — BANKBARODA":"BANKBARODA.NS",
    "BANKINDIA — BANKINDIA":"BANKINDIA.NS",
    "BATAINDIA — BATAINDIA":"BATAINDIA.NS",
    "BAYERCROP — BAYERCROP":"BAYERCROP.NS",
    "BBOX — BBOX":"BBOX.NS",
    "BCLIND — BCLIND":"BCLIND.NS",
    "BDL — BDL":"BDL.NS",
    "BEL — BEL":"BEL.NS",
    "BEML — BEML":"BEML.NS",
    "BERGEPAINT — BERGEPAINT":"BERGEPAINT.NS",
    "BFINVEST — BFINVEST":"BFINVEST.NS",
    "BHARATFORG — BHARATFORG":"BHARATFORG.NS",
    "Bharti Airtel — BHARTIARTL":"BHARTIARTL.NS",
    "BHEL — BHEL":"BHEL.NS",
    "BIOCON — BIOCON":"BIOCON.NS",
    "BIRLACORPN — BIRLACORPN":"BIRLACORPN.NS",
    "BIRLAMONEY — BIRLAMONEY":"BIRLAMONEY.NS",
    "BLUEDART — BLUEDART":"BLUEDART.NS",
    "BLUESTARCO — BLUESTARCO":"BLUESTARCO.NS",
    "BOROLTD — BOROLTD":"BOROLTD.NS",
    "BORORENEW — BORORENEW":"BORORENEW.NS",
    "BOSCHLTD — BOSCHLTD":"BOSCHLTD.NS",
    "BPCL — BPCL":"BPCL.NS",
    "BPL — BPL":"BPL.NS",
    "BRIGADE — BRIGADE":"BRIGADE.NS",
    "BRITANNIA — BRITANNIA":"BRITANNIA.NS",
    "BSE — BSE":"BSE.NS",
    "BSESME — BSESME":"BSESME.NS",
    "CAMS — CAMS":"CAMS.NS",
    "CANBK — CANBK":"CANBK.NS",
    "CANFINHOME — CANFINHOME":"CANFINHOME.NS",
    "CAPLIPOINT — CAPLIPOINT":"CAPLIPOINT.NS",
    "CARBORUNIV — CARBORUNIV":"CARBORUNIV.NS",
    "CAREERP — CAREERP":"CAREERP.NS",
    "CARYSIL — CARYSIL":"CARYSIL.NS",
    "CASTROLIND — CASTROLIND":"CASTROLIND.NS",
    "CDSL — CDSL":"CDSL.NS",
    "CEATL — CEATL":"CEATL.NS",
    "CEMENT — CEMENT":"CEMENT.NS",
    "CENTUM — CENTUM":"CENTUM.NS",
    "CERA — CERA":"CERA.NS",
    "CESC — CESC":"CESC.NS",
    "CGPOWER — CGPOWER":"CGPOWER.NS",
    "CHALET — CHALET":"CHALET.NS",
    "CHAMBLFERT — CHAMBLFERT":"CHAMBLFERT.NS",
    "CHEMPLAST — CHEMPLAST":"CHEMPLAST.NS",
    "CHOLAFIN — CHOLAFIN":"CHOLAFIN.NS",
    "CIGNITITEC — CIGNITITEC":"CIGNITITEC.NS",
    "CIPLA — CIPLA":"CIPLA.NS",
    "CLEAN — CLEAN":"CLEAN.NS",
    "CLSEL — CLSEL":"CLSEL.NS",
    "CMSINFO — CMSINFO":"CMSINFO.NS",
    "COALINDIA — COALINDIA":"COALINDIA.NS",
    "COASTCORP — COASTCORP":"COASTCORP.NS",
    "COCHINSHIP — COCHINSHIP":"COCHINSHIP.NS",
    "COFORGE — COFORGE":"COFORGE.NS",
    "COLPAL — COLPAL":"COLPAL.NS",
    "CONCOR — CONCOR":"CONCOR.NS",
    "CONSUMER — CONSUMER":"CONSUMER.NS",
    "CORALFINAC — CORALFINAC":"CORALFINAC.NS",
    "COROMANDEL — COROMANDEL":"COROMANDEL.NS",
    "CRAFTSMAN — CRAFTSMAN":"CRAFTSMAN.NS",
    "CREDITACC — CREDITACC":"CREDITACC.NS",
    "CREST — CREST":"CREST.NS",
    "CROMPTON — CROMPTON":"CROMPTON.NS",
    "CROWN — CROWN":"CROWN.NS",
    "CUB — CUB":"CUB.NS",
    "CUBEX — CUBEX":"CUBEX.NS",
    "CUMMINSIND — CUMMINSIND":"CUMMINSIND.NS",
    "CYCLOPHARM — CYCLOPHARM":"CYCLOPHARM.NS",
    "CYIENT — CYIENT":"CYIENT.NS",
    "DABUR — DABUR":"DABUR.NS",
    "DALBHARAT — DALBHARAT":"DALBHARAT.NS",
    "DATAPATTNS — DATAPATTNS":"DATAPATTNS.NS",
    "DBCORP — DBCORP":"DBCORP.NS",
    "DCAL — DCAL":"DCAL.NS",
    "DCI — DCI":"DCI.NS",
    "DCMNVL — DCMNVL":"DCMNVL.NS",
    "DCM Shriram — DCMSHRIRAM":"DCMSHRIRAM.NS",
    "DECCANCE — DECCANCE":"DECCANCE.NS",
    "DEEPAKFERT — DEEPAKFERT":"DEEPAKFERT.NS",
    "DEEPAKNTR — DEEPAKNTR":"DEEPAKNTR.NS",
    "DELHIVERY — DELHIVERY":"DELHIVERY.NS",
    "DELTACORP — DELTACORP":"DELTACORP.NS",
    "DEN — DEN":"DEN.NS",
    "DENORA — DENORA":"DENORA.NS",
    "DENTALKART — DENTALKART":"DENTALKART.NS",
    "DEVYANI — DEVYANI":"DEVYANI.NS",
    "DHAMPURSUG — DHAMPURSUG":"DHAMPURSUG.NS",
    "DHANI — DHANI":"DHANI.NS",
    "DHANUKA — DHANUKA":"DHANUKA.NS",
    "DHARMAJ — DHARMAJ":"DHARMAJ.NS",
    "DHRUV — DHRUV":"DHRUV.NS",
    "DIVISLAB — DIVISLAB":"DIVISLAB.NS",
    "DIXON — DIXON":"DIXON.NS",
    "DLF — DLF":"DLF.NS",
    "DMART — DMART":"DMART.NS",
    "DODLA — DODLA":"DODLA.NS",
    "DOLLAR — DOLLAR":"DOLLAR.NS",
    "DRREDDY — DRREDDY":"DRREDDY.NS",
    "EASEMYTRIP — EASEMYTRIP":"EASEMYTRIP.NS",
    "EASTSILK — EASTSILK":"EASTSILK.NS",
    "ECLERX — ECLERX":"ECLERX.NS",
    "EDELWEISS — EDELWEISS":"EDELWEISS.NS",
    "EFC — EFC":"EFC.NS",
    "EFORCE — EFORCE":"EFORCE.NS",
    "EICHERMOT — EICHERMOT":"EICHERMOT.NS",
    "EIDPARRY — EIDPARRY":"EIDPARRY.NS",
    "EIHOTEL — EIHOTEL":"EIHOTEL.NS",
    "EIMCOELECO — EIMCOELECO":"EIMCOELECO.NS",
    "ELECON — ELECON":"ELECON.NS",
    "ELECTCAST — ELECTCAST":"ELECTCAST.NS",
    "ELGIEQUIP — ELGIEQUIP":"ELGIEQUIP.NS",
    "EMAMILTD — EMAMILTD":"EMAMILTD.NS",
    "EMKAY — EMKAY":"EMKAY.NS",
    "ENDURANCE — ENDURANCE":"ENDURANCE.NS",
    "ENGINERS — ENGINERS":"ENGINERS.NS",
    "ENIL — ENIL":"ENIL.NS",
    "ENRIN — ENRIN":"ENRIN.NS",
    "EPIGRAL — EPIGRAL":"EPIGRAL.NS",
    "EPL — EPL":"EPL.NS",
    "EQUITASBNK — EQUITASBNK":"EQUITASBNK.NS",
    "ERIS — ERIS":"ERIS.NS",
    "ESABINDIA — ESABINDIA":"ESABINDIA.NS",
    "ESCORTS — ESCORTS":"ESCORTS.NS",
    "ETERNAL — ETERNAL":"ETERNAL.NS",
    "EVEREADY — EVEREADY":"EVEREADY.NS",
    "EXCELINDUS — EXCELINDUS":"EXCELINDUS.NS",
    "EXIDEIND — EXIDEIND":"EXIDEIND.NS",
    "FACT — FACT":"FACT.NS",
    "FAIRFIELD — FAIRFIELD":"FAIRFIELD.NS",
    "FCL — FCL":"FCL.NS",
    "FDC — FDC":"FDC.NS",
    "FEDERALBNK — FEDERALBNK":"FEDERALBNK.NS",
    "FEL — FEL":"FEL.NS",
    "FIBERWEB — FIBERWEB":"FIBERWEB.NS",
    "FINCABLES — FINCABLES":"FINCABLES.NS",
    "FINEORG — FINEORG":"FINEORG.NS",
    "FINPIPE — FINPIPE":"FINPIPE.NS",
    "FOCUS — FOCUS":"FOCUS.NS",
    "FORTIS — FORTIS":"FORTIS.NS",
    "FSL — FSL":"FSL.NS",
    "FUSION — FUSION":"FUSION.NS",
    "GABRIEL — GABRIEL":"GABRIEL.NS",
    "GAIL — GAIL":"GAIL.NS",
    "GALAXYSURF — GALAXYSURF":"GALAXYSURF.NS",
    "GALLANTT — GALLANTT":"GALLANTT.NS",
    "GANDHITUBE — GANDHITUBE":"GANDHITUBE.NS",
    "GARFIBRES — GARFIBRES":"GARFIBRES.NS",
    "GEOJIT — GEOJIT":"GEOJIT.NS",
    "GEPIL — GEPIL":"GEPIL.NS",
    "GESHIP — GESHIP":"GESHIP.NS",
    "GHCL — GHCL":"GHCL.NS",
    "GICHSGFIN — GICHSGFIN":"GICHSGFIN.NS",
    "GICRE — GICRE":"GICRE.NS",
    "GILLETTE — GILLETTE":"GILLETTE.NS",
    "GKWLIMITED — GKWLIMITED":"GKWLIMITED.NS",
    "GLAND — GLAND":"GLAND.NS",
    "GLENMARK — GLENMARK":"GLENMARK.NS",
    "GLOBAL — GLOBAL":"GLOBAL.NS",
    "GLOBUSSPR — GLOBUSSPR":"GLOBUSSPR.NS",
    "GMDCLTD — GMDCLTD":"GMDCLTD.NS",
    "GMRAIRPORT — GMRAIRPORT":"GMRAIRPORT.NS",
    "GOCLCORP — GOCLCORP":"GOCLCORP.NS",
    "GODFRYPHLP — GODFRYPHLP":"GODFRYPHLP.NS",
    "GODREJAGRO — GODREJAGRO":"GODREJAGRO.NS",
    "GODREJCP — GODREJCP":"GODREJCP.NS",
    "GODREJIND — GODREJIND":"GODREJIND.NS",
    "GODREJPROP — GODREJPROP":"GODREJPROP.NS",
    "GOKEX — GOKEX":"GOKEX.NS",
    "GOLDIAM — GOLDIAM":"GOLDIAM.NS",
    "GPIL — GPIL":"GPIL.NS",
    "GRANULES — GRANULES":"GRANULES.NS",
    "GRAPHITE — GRAPHITE":"GRAPHITE.NS",
    "GRASIM — GRASIM":"GRASIM.NS",
    "GRAVITA — GRAVITA":"GRAVITA.NS",
    "GREENPANEL — GREENPANEL":"GREENPANEL.NS",
    "GRINDWELL — GRINDWELL":"GRINDWELL.NS",
    "GROWW — GROWW":"GROWW.NS",
    "GSFC — GSFC":"GSFC.NS",
    "GSPL — GSPL":"GSPL.NS",
    "GUJGASLTD — GUJGASLTD":"GUJGASLTD.NS",
    "GVT&D — GVT&D":"GVT&D.NS",
    "HAL — HAL":"HAL.NS",
    "HAPPSTMNDS — HAPPSTMNDS":"HAPPSTMNDS.NS",
    "HATHWAY — HATHWAY":"HATHWAY.NS",
    "HATSUN — HATSUN":"HATSUN.NS",
    "HAVELLS — HAVELLS":"HAVELLS.NS",
    "HBLENGINE — HBLENGINE":"HBLENGINE.NS",
    "HCG — HCG":"HCG.NS",
    "HCLTECH — HCLTECH":"HCLTECH.NS",
    "HDFCAMC — HDFCAMC":"HDFCAMC.NS",
    "HDFC Bank — HDFCBANK":"HDFCBANK.NS",
    "HDFCLIFE — HDFCLIFE":"HDFCLIFE.NS",
    "HEG — HEG":"HEG.NS",
    "HERCULES — HERCULES":"HERCULES.NS",
    "HEROMOTOCO — HEROMOTOCO":"HEROMOTOCO.NS",
    "HFCL — HFCL":"HFCL.NS",
    "HINDALCO — HINDALCO":"HINDALCO.NS",
    "HINDCOPPER — HINDCOPPER":"HINDCOPPER.NS",
    "HINDMOTORS — HINDMOTORS":"HINDMOTORS.NS",
    "HINDPETRO — HINDPETRO":"HINDPETRO.NS",
    "Hindustan Unilever — HINDUNILVR":"HINDUNILVR.NS",
    "HINDWAREAP — HINDWAREAP":"HINDWAREAP.NS",
    "HINDZINC — HINDZINC":"HINDZINC.NS",
    "HIRECT — HIRECT":"HIRECT.NS",
    "HITECH — HITECH":"HITECH.NS",
    "HLEGLAS — HLEGLAS":"HLEGLAS.NS",
    "HMT — HMT":"HMT.NS",
    "HMVL — HMVL":"HMVL.NS",
    "HOMEFIRST — HOMEFIRST":"HOMEFIRST.NS",
    "HONASA — HONASA":"HONASA.NS",
    "HONAUT — HONAUT":"HONAUT.NS",
    "HPL — HPL":"HPL.NS",
    "HUDCO — HUDCO":"HUDCO.NS",
    "HYUNDAI — HYUNDAI":"HYUNDAI.NS",
    "ICICI Bank — ICICIBANK":"ICICIBANK.NS",
    "ICICIGI — ICICIGI":"ICICIGI.NS",
    "ICICIPRULI — ICICIPRULI":"ICICIPRULI.NS",
    "ICRA — ICRA":"ICRA.NS",
    "IDBI — IDBI":"IDBI.NS",
    "IDEA — IDEA":"IDEA.NS",
    "IDFCFIRSTB — IDFCFIRSTB":"IDFCFIRSTB.NS",
    "IEX — IEX":"IEX.NS",
    "IFCI — IFCI":"IFCI.NS",
    "IGL — IGL":"IGL.NS",
    "IIFL — IIFL":"IIFL.NS",
    "IIFLSEC — IIFLSEC":"IIFLSEC.NS",
    "IKS — IKS":"IKS.NS",
    "INDHOTEL — INDHOTEL":"INDHOTEL.NS",
    "INDIAMART — INDIAMART":"INDIAMART.NS",
    "INDIANB — INDIANB":"INDIANB.NS",
    "INDIGO — INDIGO":"INDIGO.NS",
    "INDOCO — INDOCO":"INDOCO.NS",
    "INDORAMA — INDORAMA":"INDORAMA.NS",
    "INDOSTAR — INDOSTAR":"INDOSTAR.NS",
    "INDUSINDBK — INDUSINDBK":"INDUSINDBK.NS",
    "INDUSTOWER — INDUSTOWER":"INDUSTOWER.NS",
    "Infosys — INFY":"INFY.NS",
    "INOXGREEN — INOXGREEN":"INOXGREEN.NS",
    "INOXINDIA — INOXINDIA":"INOXINDIA.NS",
    "INOXWIND — INOXWIND":"INOXWIND.NS",
    "INSECTICID — INSECTICID":"INSECTICID.NS",
    "INSPIRIS — INSPIRIS":"INSPIRIS.NS",
    "INTELLECT — INTELLECT":"INTELLECT.NS",
    "IOC — IOC":"IOC.NS",
    "IRCTC — IRCTC":"IRCTC.NS",
    "IRFC — IRFC":"IRFC.NS",
    "ITC — ITC":"ITC.NS",
    "JAGSNPHARM — JAGSNPHARM":"JAGSNPHARM.NS",
    "JAYBARMARU — JAYBARMARU":"JAYBARMARU.NS",
    "JAYNECO — JAYNECO":"JAYNECO.NS",
    "JBCHEPHARM — JBCHEPHARM":"JBCHEPHARM.NS",
    "JCHAC — JCHAC":"JCHAC.NS",
    "JINDALSAW — JINDALSAW":"JINDALSAW.NS",
    "JINDALSTEL — JINDALSTEL":"JINDALSTEL.NS",
    "JINDWORLD — JINDWORLD":"JINDWORLD.NS",
    "JIOFIN — JIOFIN":"JIOFIN.NS",
    "JISLJALEQS — JISLJALEQS":"JISLJALEQS.NS",
    "JK — JK":"JK.NS",
    "JKCEMENT — JKCEMENT":"JKCEMENT.NS",
    "JKLAKSHMI — JKLAKSHMI":"JKLAKSHMI.NS",
    "JKPAPER — JKPAPER":"JKPAPER.NS",
    "JKTYRE — JKTYRE":"JKTYRE.NS",
    "JMA — JMA":"JMA.NS",
    "JMFINANCIL — JMFINANCIL":"JMFINANCIL.NS",
    "JSL — JSL":"JSL.NS",
    "JSWENERGY — JSWENERGY":"JSWENERGY.NS",
    "JSWSTEEL — JSWSTEEL":"JSWSTEEL.NS",
    "JTEKTINDIA — JTEKTINDIA":"JTEKTINDIA.NS",
    "JUBLFOOD — JUBLFOOD":"JUBLFOOD.NS",
    "JUSTDIAL — JUSTDIAL":"JUSTDIAL.NS",
    "KABRAEXTRU — KABRAEXTRU":"KABRAEXTRU.NS",
    "KALPATPOWR — KALPATPOWR":"KALPATPOWR.NS",
    "KALYANKJIL — KALYANKJIL":"KALYANKJIL.NS",
    "KAMATHOTEL — KAMATHOTEL":"KAMATHOTEL.NS",
    "KANORICHEM — KANORICHEM":"KANORICHEM.NS",
    "KANSAINER — KANSAINER":"KANSAINER.NS",
    "KAYNES — KAYNES":"KAYNES.NS",
    "KDDL — KDDL":"KDDL.NS",
    "KEC — KEC":"KEC.NS",
    "KEI — KEI":"KEI.NS",
    "KELLTON — KELLTON":"KELLTON.NS",
    "KERNEX — KERNEX":"KERNEX.NS",
    "KESORAM — KESORAM":"KESORAM.NS",
    "KFINTECH — KFINTECH":"KFINTECH.NS",
    "KHAICHEM — KHAICHEM":"KHAICHEM.NS",
    "KILITCH — KILITCH":"KILITCH.NS",
    "KINGFA — KINGFA":"KINGFA.NS",
    "KIOCL — KIOCL":"KIOCL.NS",
    "KIRLOSBROS — KIRLOSBROS":"KIRLOSBROS.NS",
    "KIRLOSENG — KIRLOSENG":"KIRLOSENG.NS",
    "KITEX — KITEX":"KITEX.NS",
    "KNRCON — KNRCON":"KNRCON.NS",
    "KOLTEPATIL — KOLTEPATIL":"KOLTEPATIL.NS",
    "KONCORDBIO — KONCORDBIO":"KONCORDBIO.NS",
    "KOPRAN — KOPRAN":"KOPRAN.NS",
    "KOTAKBANK — KOTAKBANK":"KOTAKBANK.NS",
    "KOTHARIPRO — KOTHARIPRO":"KOTHARIPRO.NS",
    "KPITTECH — KPITTECH":"KPITTECH.NS",
    "KPRMILL — KPRMILL":"KPRMILL.NS",
    "KRBL — KRBL":"KRBL.NS",
    "KRIDHAN — KRIDHAN":"KRIDHAN.NS",
    "LALPATHLAB — LALPATHLAB":"LALPATHLAB.NS",
    "LAURUSLABS — LAURUSLABS":"LAURUSLABS.NS",
    "LAXMIMACH — LAXMIMACH":"LAXMIMACH.NS",
    "LCCINFOTEC — LCCINFOTEC":"LCCINFOTEC.NS",
    "LEMONTREE — LEMONTREE":"LEMONTREE.NS",
    "LICHSGFIN — LICHSGFIN":"LICHSGFIN.NS",
    "LICI — LICI":"LICI.NS",
    "LLOYDSENGG — LLOYDSENGG":"LLOYDSENGG.NS",
    "LLOYDSME — LLOYDSME":"LLOYDSME.NS",
    "LODHA — LODHA":"LODHA.NS",
    "LOKESHMACH — LOKESHMACH":"LOKESHMACH.NS",
    "Larsen & Toubro — LT":"LT.NS",
    "LTF — LTF":"LTF.NS",
    "LTM — LTM":"LTM.NS",
    "LTTS — LTTS":"LTTS.NS",
    "LUMAXTECH — LUMAXTECH":"LUMAXTECH.NS",
    "LUPIN — LUPIN":"LUPIN.NS",
    "LUXIND — LUXIND":"LUXIND.NS",
    "M&M — M&M":"M&M.NS",
    "M&MFIN — M&MFIN":"M&MFIN.NS",
    "MAFANG — MAFANG":"MAFANG.NS",
    "MAFSETF — MAFSETF":"MAFSETF.NS",
    "MAHABANK — MAHABANK":"MAHABANK.NS",
    "MAHLOG — MAHLOG":"MAHLOG.NS",
    "MAHSCOOTER — MAHSCOOTER":"MAHSCOOTER.NS",
    "MAHSEAMLES — MAHSEAMLES":"MAHSEAMLES.NS",
    "MAITHANALL — MAITHANALL":"MAITHANALL.NS",
    "MANAPPURAM — MANAPPURAM":"MANAPPURAM.NS",
    "MANINDS — MANINDS":"MANINDS.NS",
    "MANKIND — MANKIND":"MANKIND.NS",
    "MARATHON — MARATHON":"MARATHON.NS",
    "MARICO — MARICO":"MARICO.NS",
    "Maruti Suzuki — MARUTI":"MARUTI.NS",
    "MASFIN — MASFIN":"MASFIN.NS",
    "MASTEK — MASTEK":"MASTEK.NS",
    "MATHEWES — MATHEWES":"MATHEWES.NS",
    "MATIX — MATIX":"MATIX.NS",
    "MAXHEALTH — MAXHEALTH":"MAXHEALTH.NS",
    "MAYURUNIQ — MAYURUNIQ":"MAYURUNIQ.NS",
    "MAZDOCK — MAZDOCK":"MAZDOCK.NS",
    "MCX — MCX":"MCX.NS",
    "MEDANTA — MEDANTA":"MEDANTA.NS",
    "MEDIASSIST — MEDIASSIST":"MEDIASSIST.NS",
    "MEP — MEP":"MEP.NS",
    "METROPOLIS — METROPOLIS":"METROPOLIS.NS",
    "MFSL — MFSL":"MFSL.NS",
    "MGL — MGL":"MGL.NS",
    "MINDACORP — MINDACORP":"MINDACORP.NS",
    "MIRZAINT — MIRZAINT":"MIRZAINT.NS",
    "MMTC — MMTC":"MMTC.NS",
    "MOIL — MOIL":"MOIL.NS",
    "MOLDTKPAC — MOLDTKPAC":"MOLDTKPAC.NS",
    "MONTECARLO — MONTECARLO":"MONTECARLO.NS",
    "MOTHERSON — MOTHERSON":"MOTHERSON.NS",
    "MOTILALOFS — MOTILALOFS":"MOTILALOFS.NS",
    "MOTOGENFIN — MOTOGENFIN":"MOTOGENFIN.NS",
    "MPHASIS — MPHASIS":"MPHASIS.NS",
    "MPSLTD — MPSLTD":"MPSLTD.NS",
    "MRF — MRF":"MRF.NS",
    "MRPL — MRPL":"MRPL.NS",
    "MSTCLTD — MSTCLTD":"MSTCLTD.NS",
    "MUTHOOTFIN — MUTHOOTFIN":"MUTHOOTFIN.NS",
    "NACLIND — NACLIND":"NACLIND.NS",
    "NAGAFERT — NAGAFERT":"NAGAFERT.NS",
    "NARMADA — NARMADA":"NARMADA.NS",
    "NATCOPHARM — NATCOPHARM":"NATCOPHARM.NS",
    "NATIONALUM — NATIONALUM":"NATIONALUM.NS",
    "NAUKRI — NAUKRI":"NAUKRI.NS",
    "NAVINFLUOR — NAVINFLUOR":"NAVINFLUOR.NS",
    "NBCC — NBCC":"NBCC.NS",
    "NCC — NCC":"NCC.NS",
    "NEOGEN — NEOGEN":"NEOGEN.NS",
    "NESTLEIND — NESTLEIND":"NESTLEIND.NS",
    "NETWORK18 — NETWORK18":"NETWORK18.NS",
    "NEULAND — NEULAND":"NEULAND.NS",
    "NEWGEN — NEWGEN":"NEWGEN.NS",
    "NGLFINE — NGLFINE":"NGLFINE.NS",
    "NHPC — NHPC":"NHPC.NS",
    "NIACL — NIACL":"NIACL.NS",
    "NILKAMAL — NILKAMAL":"NILKAMAL.NS",
    "NIRLON — NIRLON":"NIRLON.NS",
    "NITCO — NITCO":"NITCO.NS",
    "NITINSPIN — NITINSPIN":"NITINSPIN.NS",
    "NLCINDIA — NLCINDIA":"NLCINDIA.NS",
    "NMDC — NMDC":"NMDC.NS",
    "NMDCSTEEL — NMDCSTEEL":"NMDCSTEEL.NS",
    "NOCIL — NOCIL":"NOCIL.NS",
    "NOVARTIND — NOVARTIND":"NOVARTIND.NS",
    "NRAIL — NRAIL":"NRAIL.NS",
    "NTPC — NTPC":"NTPC.NS",
    "NYKAA — NYKAA":"NYKAA.NS",
    "OAL — OAL":"OAL.NS",
    "OBEROIRLTY — OBEROIRLTY":"OBEROIRLTY.NS",
    "OFSS — OFSS":"OFSS.NS",
    "OIL — OIL":"OIL.NS",
    "OLAELEC — OLAELEC":"OLAELEC.NS",
    "ONGC — ONGC":"ONGC.NS",
    "ORCHPHARMA — ORCHPHARMA":"ORCHPHARMA.NS",
    "ORIENTCEM — ORIENTCEM":"ORIENTCEM.NS",
    "ORIENTELEC — ORIENTELEC":"ORIENTELEC.NS",
    "ORIENTHOT — ORIENTHOT":"ORIENTHOT.NS",
    "ORIENTPPR — ORIENTPPR":"ORIENTPPR.NS",
    "OSWALGREEN — OSWALGREEN":"OSWALGREEN.NS",
    "PAGEIND — PAGEIND":"PAGEIND.NS",
    "PAISALO — PAISALO":"PAISALO.NS",
    "PAKKA — PAKKA":"PAKKA.NS",
    "PARAGMILK — PARAGMILK":"PARAGMILK.NS",
    "PARAS — PARAS":"PARAS.NS",
    "PARSVNATH — PARSVNATH":"PARSVNATH.NS",
    "PATANJALI — PATANJALI":"PATANJALI.NS",
    "PATELENG — PATELENG":"PATELENG.NS",
    "PAYTM — PAYTM":"PAYTM.NS",
    "PCBL — PCBL":"PCBL.NS",
    "PEL — PEL":"PEL.NS",
    "PERSISTENT — PERSISTENT":"PERSISTENT.NS",
    "PETRONET — PETRONET":"PETRONET.NS",
    "PFC — PFC":"PFC.NS",
    "PFIZER — PFIZER":"PFIZER.NS",
    "PFOCUS — PFOCUS":"PFOCUS.NS",
    "PFS — PFS":"PFS.NS",
    "PGEL — PGEL":"PGEL.NS",
    "PHOENIXLTD — PHOENIXLTD":"PHOENIXLTD.NS",
    "PIDILITIND — PIDILITIND":"PIDILITIND.NS",
    "PIGL — PIGL":"PIGL.NS",
    "PIIND — PIIND":"PIIND.NS",
    "PINELABS — PINELABS":"PINELABS.NS",
    "PIONEEREMB — PIONEEREMB":"PIONEEREMB.NS",
    "PLASTIBLEN — PLASTIBLEN":"PLASTIBLEN.NS",
    "PNB — PNB":"PNB.NS",
    "PNBHOUSING — PNBHOUSING":"PNBHOUSING.NS",
    "PNCINFRA — PNCINFRA":"PNCINFRA.NS",
    "POKARNA — POKARNA":"POKARNA.NS",
    "POLICYBZR — POLICYBZR":"POLICYBZR.NS",
    "POLYCAB — POLYCAB":"POLYCAB.NS",
    "POLYMED — POLYMED":"POLYMED.NS",
    "POWERGRID — POWERGRID":"POWERGRID.NS",
    "PRAJIND — PRAJIND":"PRAJIND.NS",
    "PRESTIGE — PRESTIGE":"PRESTIGE.NS",
    "PRICOLLTD — PRICOLLTD":"PRICOLLTD.NS",
    "PRINCEPIPE — PRINCEPIPE":"PRINCEPIPE.NS",
    "PRSMJOHNSN — PRSMJOHNSN":"PRSMJOHNSN.NS",
    "PTC — PTC":"PTC.NS",
    "QUESS — QUESS":"QUESS.NS",
    "RACLGEAR — RACLGEAR":"RACLGEAR.NS",
    "RADICO — RADICO":"RADICO.NS",
    "RAIN — RAIN":"RAIN.NS",
    "RAJESHEXPO — RAJESHEXPO":"RAJESHEXPO.NS",
    "RALLIS — RALLIS":"RALLIS.NS",
    "RANEHOLDIN — RANEHOLDIN":"RANEHOLDIN.NS",
    "RATNAMANI — RATNAMANI":"RATNAMANI.NS",
    "RAYMOND — RAYMOND":"RAYMOND.NS",
    "RBA — RBA":"RBA.NS",
    "RBLBANK — RBLBANK":"RBLBANK.NS",
    "RCF — RCF":"RCF.NS",
    "RECLTD — RECLTD":"RECLTD.NS",
    "REDINGTON — REDINGTON":"REDINGTON.NS",
    "REGENCERAM — REGENCERAM":"REGENCERAM.NS",
    "RELAXO — RELAXO":"RELAXO.NS",
    "Reliance Industries — RELIANCE":"RELIANCE.NS",
    "REMSONS — REMSONS":"REMSONS.NS",
    "RESPONIND — RESPONIND":"RESPONIND.NS",
    "RICOAUTO — RICOAUTO":"RICOAUTO.NS",
    "RISHABH — RISHABH":"RISHABH.NS",
    "RITES — RITES":"RITES.NS",
    "RKFORGE — RKFORGE":"RKFORGE.NS",
    "ROHLTD — ROHLTD":"ROHLTD.NS",
    "ROSSARI — ROSSARI":"ROSSARI.NS",
    "ROUTE — ROUTE":"ROUTE.NS",
    "RPGLIFE — RPGLIFE":"RPGLIFE.NS",
    "RPOWER — RPOWER":"RPOWER.NS",
    "RPPINFRA — RPPINFRA":"RPPINFRA.NS",
    "RSYSTEMS — RSYSTEMS":"RSYSTEMS.NS",
    "RVNL — RVNL":"RVNL.NS",
    "SAIL — SAIL":"SAIL.NS",
    "SANDUMA — SANDUMA":"SANDUMA.NS",
    "SANGHIIND — SANGHIIND":"SANGHIIND.NS",
    "SANGHVIMOV — SANGHVIMOV":"SANGHVIMOV.NS",
    "SANOFI — SANOFI":"SANOFI.NS",
    "SANSERA — SANSERA":"SANSERA.NS",
    "SARDAEN — SARDAEN":"SARDAEN.NS",
    "SASKEN — SASKEN":"SASKEN.NS",
    "SATIA — SATIA":"SATIA.NS",
    "SBICARD — SBICARD":"SBICARD.NS",
    "SBILIFE — SBILIFE":"SBILIFE.NS",
    "State Bank of India — SBIN":"SBIN.NS",
    "SCHAEFFLER — SCHAEFFLER":"SCHAEFFLER.NS",
    "SCHNEIDER — SCHNEIDER":"SCHNEIDER.NS",
    "SCI — SCI":"SCI.NS",
    "SFL — SFL":"SFL.NS",
    "SHALBY — SHALBY":"SHALBY.NS",
    "SHANKARA — SHANKARA":"SHANKARA.NS",
    "SHANTIGEAR — SHANTIGEAR":"SHANTIGEAR.NS",
    "SHARDACROP — SHARDACROP":"SHARDACROP.NS",
    "SHILPAMED — SHILPAMED":"SHILPAMED.NS",
    "SHOPERSTOP — SHOPERSTOP":"SHOPERSTOP.NS",
    "SHREDIGCEM — SHREDIGCEM":"SHREDIGCEM.NS",
    "SHREECEM — SHREECEM":"SHREECEM.NS",
    "SHRIRAMFIN — SHRIRAMFIN":"SHRIRAMFIN.NS",
    "SHYAMMETL — SHYAMMETL":"SHYAMMETL.NS",
    "SICAL — SICAL":"SICAL.NS",
    "SIEMENS — SIEMENS":"SIEMENS.NS",
    "SIGNATURE — SIGNATURE":"SIGNATURE.NS",
    "SIL — SIL":"SIL.NS",
    "SIRCA — SIRCA":"SIRCA.NS",
    "SJS — SJS":"SJS.NS",
    "SJVN — SJVN":"SJVN.NS",
    "SKFINDIA — SKFINDIA":"SKFINDIA.NS",
    "SMLISUZU — SMLISUZU":"SMLISUZU.NS",
    "SOLARINDS — SOLARINDS":"SOLARINDS.NS",
    "SONACOMS — SONACOMS":"SONACOMS.NS",
    "SONATSOFTW — SONATSOFTW":"SONATSOFTW.NS",
    "SPAL — SPAL":"SPAL.NS",
    "SPEL — SPEL":"SPEL.NS",
    "SPENCERS — SPENCERS":"SPENCERS.NS",
    "SPIC — SPIC":"SPIC.NS",
    "SRF — SRF":"SRF.NS",
    "STARCEMENT — STARCEMENT":"STARCEMENT.NS",
    "STARHEALTH — STARHEALTH":"STARHEALTH.NS",
    "STLTECH — STLTECH":"STLTECH.NS",
    "SUBROS — SUBROS":"SUBROS.NS",
    "SUDARSCHEM — SUDARSCHEM":"SUDARSCHEM.NS",
    "SUMICHEM — SUMICHEM":"SUMICHEM.NS",
    "SUNDARMFIN — SUNDARMFIN":"SUNDARMFIN.NS",
    "SUNDRMFAST — SUNDRMFAST":"SUNDRMFAST.NS",
    "SUNFLAG — SUNFLAG":"SUNFLAG.NS",
    "SUNPHARMA — SUNPHARMA":"SUNPHARMA.NS",
    "SUNTV — SUNTV":"SUNTV.NS",
    "SUPRAJIT — SUPRAJIT":"SUPRAJIT.NS",
    "SUPREMEIND — SUPREMEIND":"SUPREMEIND.NS",
    "SUTLEJTEX — SUTLEJTEX":"SUTLEJTEX.NS",
    "SUZLON — SUZLON":"SUZLON.NS",
    "SWANENERGY — SWANENERGY":"SWANENERGY.NS",
    "SWARAJENG — SWARAJENG":"SWARAJENG.NS",
    "SWIGGY — SWIGGY":"SWIGGY.NS",
    "SYMPHONY — SYMPHONY":"SYMPHONY.NS",
    "SYNGENE — SYNGENE":"SYNGENE.NS",
    "TARC — TARC":"TARC.NS",
    "TASTYBITE — TASTYBITE":"TASTYBITE.NS",
    "TATACAPITAL — TATACAPITAL":"TATACAPITAL.NS",
    "TATACHEM — TATACHEM":"TATACHEM.NS",
    "TATACOMM — TATACOMM":"TATACOMM.NS",
    "TATACONSUM — TATACONSUM":"TATACONSUM.NS",
    "TATAELXSI — TATAELXSI":"TATAELXSI.NS",
    "Tata Motors — TATAMOTORS":"TATAMOTORS.NS",
    "TATAPOWER — TATAPOWER":"TATAPOWER.NS",
    "TATASTEEL — TATASTEEL":"TATASTEEL.NS",
    "TATVA — TATVA":"TATVA.NS",
    "Tata Consultancy Services — TCS":"TCS.NS",
    "TEAMLEASE — TEAMLEASE":"TEAMLEASE.NS",
    "TECHM — TECHM":"TECHM.NS",
    "TEJASNET — TEJASNET":"TEJASNET.NS",
    "TGBHOTELS — TGBHOTELS":"TGBHOTELS.NS",
    "THANGAMAYL — THANGAMAYL":"THANGAMAYL.NS",
    "THERMAX — THERMAX":"THERMAX.NS",
    "THOMASCOOK — THOMASCOOK":"THOMASCOOK.NS",
    "THYROCARE — THYROCARE":"THYROCARE.NS",
    "TIDEWATER — TIDEWATER":"TIDEWATER.NS",
    "TIINDIA — TIINDIA":"TIINDIA.NS",
    "TIMKEN — TIMKEN":"TIMKEN.NS",
    "TITAN — TITAN":"TITAN.NS",
    "TMPV — TMPV":"TMPV.NS",
    "TOKYOPLAST — TOKYOPLAST":"TOKYOPLAST.NS",
    "TORNTPHARM — TORNTPHARM":"TORNTPHARM.NS",
    "TRANSWORLD — TRANSWORLD":"TRANSWORLD.NS",
    "TRENT — TRENT":"TRENT.NS",
    "TRIDENT — TRIDENT":"TRIDENT.NS",
    "TRITURBINE — TRITURBINE":"TRITURBINE.NS",
    "TRU — TRU":"TRU.NS",
    "TTKPRESTIG — TTKPRESTIG":"TTKPRESTIG.NS",
    "TVSMOTOR — TVSMOTOR":"TVSMOTOR.NS",
    "TVSSCS — TVSSCS":"TVSSCS.NS",
    "UBL — UBL":"UBL.NS",
    "UCOBANK — UCOBANK":"UCOBANK.NS",
    "UDS — UDS":"UDS.NS",
    "UJJIVANSFB — UJJIVANSFB":"UJJIVANSFB.NS",
    "ULTRACEMCO — ULTRACEMCO":"ULTRACEMCO.NS",
    "UNICHEMLAB — UNICHEMLAB":"UNICHEMLAB.NS",
    "UNIONBANK — UNIONBANK":"UNIONBANK.NS",
    "UNITDSPR — UNITDSPR":"UNITDSPR.NS",
    "UNOMINDA — UNOMINDA":"UNOMINDA.NS",
    "UPL — UPL":"UPL.NS",
    "URJA — URJA":"URJA.NS",
    "VADILAL — VADILAL":"VADILAL.NS",
    "VAKRANGEE — VAKRANGEE":"VAKRANGEE.NS",
    "VARDHACRLC — VARDHACRLC":"VARDHACRLC.NS",
    "VARROC — VARROC":"VARROC.NS",
    "VASCONEQ — VASCONEQ":"VASCONEQ.NS",
    "VAXFAB — VAXFAB":"VAXFAB.NS",
    "VBL — VBL":"VBL.NS",
    "Vedanta — VEDL":"VEDL.NS",
    "VESUVIUS — VESUVIUS":"VESUVIUS.NS",
    "VGUARD — VGUARD":"VGUARD.NS",
    "VINATIORGA — VINATIORGA":"VINATIORGA.NS",
    "VIPIND — VIPIND":"VIPIND.NS",
    "VLSFINANCE — VLSFINANCE":"VLSFINANCE.NS",
    "VMART — VMART":"VMART.NS",
    "VOLTAMP — VOLTAMP":"VOLTAMP.NS",
    "VOLTAS — VOLTAS":"VOLTAS.NS",
    "WABAG — WABAG":"WABAG.NS",
    "WEALTH — WEALTH":"WEALTH.NS",
    "WELCORP — WELCORP":"WELCORP.NS",
    "WELSPUNLIV — WELSPUNLIV":"WELSPUNLIV.NS",
    "WENDT — WENDT":"WENDT.NS",
    "WESTLIFE — WESTLIFE":"WESTLIFE.NS",
    "WHIRLPOOL — WHIRLPOOL":"WHIRLPOOL.NS",
    "WINDLAS — WINDLAS":"WINDLAS.NS",
    "WIPRO — WIPRO":"WIPRO.NS",
    "WSI — WSI":"WSI.NS",
    "WSTCSTP — WSTCSTP":"WSTCSTP.NS",
    "XCHANGING — XCHANGING":"XCHANGING.NS",
    "YESBANK — YESBANK":"YESBANK.NS",
    "ZAGGLE — ZAGGLE":"ZAGGLE.NS",
    "ZENSARTECH — ZENSARTECH":"ZENSARTECH.NS",
    "ZENTEC — ZENTEC":"ZENTEC.NS",
    "ZYDUSLIFE — ZYDUSLIFE":"ZYDUSLIFE.NS"
}
FEATS=["ret1","ret3","ret5","ema_gap","ema_slope","rsi","macd_hist","atr_pct","vol_ratio","range_pct"]
def clean(d):
    if d is None or d.empty:return pd.DataFrame()
    if isinstance(d.columns,pd.MultiIndex): d.columns=d.columns.get_level_values(0)
    d=d.rename(columns={c:str(c).title() for c in d.columns})
    cols=["Open","High","Low","Close","Volume"]
    if not all(c in d for c in cols):return pd.DataFrame()
    for c in cols:d[c]=pd.to_numeric(d[c],errors="coerce")
    return d[cols].dropna(subset=["Open","High","Low","Close"])
@st.cache_data(ttl=300,show_spinner=False)
def daily(t):return clean(yf.download(t,period="3y",interval="1d",auto_adjust=True,progress=False,threads=False))
@st.cache_data(ttl=90,show_spinner=False)
def intra(t):return clean(yf.download(t,period="5d",interval="5m",auto_adjust=True,progress=False,threads=False))
def features(d):
    x=d.copy();c,h,l,v=x.Close,x.High,x.Low,x.Volume
    x["ret1"]=c.pct_change();x["ret3"]=c.pct_change(3);x["ret5"]=c.pct_change(5)
    e20=c.ewm(span=20,adjust=False).mean();e50=c.ewm(span=50,adjust=False).mean()
    x["ema_gap"]=e20/e50-1;x["ema_slope"]=e20.pct_change(5)
    delta=c.diff();gain=delta.clip(lower=0).ewm(alpha=1/14,adjust=False).mean();loss=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean()
    x["rsi"]=100-100/(1+gain/loss.replace(0,np.nan))
    macd=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean()
    x["macd_hist"]=(macd-macd.ewm(span=9,adjust=False).mean())/c
    prev=c.shift();tr=pd.concat([h-l,(h-prev).abs(),(l-prev).abs()],axis=1).max(axis=1)
    x["atr"]=tr.rolling(14).mean();x["atr_pct"]=x.atr/c
    x["vol_ratio"]=v/v.rolling(20).mean();x["range_pct"]=(h-l)/c
    x["ema20"]=e20;x["ema50"]=e50
    return x
def analyze(t):
    d=daily(t)
    if len(d)<220:raise ValueError("Insufficient daily history or data unavailable.")
    f=features(d);f["target"]=(f.Close.shift(-1)>f.Close).astype(int)
    data=f.dropna(subset=FEATS+["target"])
    if len(data)<180:raise ValueError("Not enough clean rows after indicators.")
    train=data.iloc[:-1];latest=f.dropna(subset=FEATS).iloc[[-1]]
    split=int(.8*len(train));tr,te=train.iloc[:split],train.iloc[split:]
    model=Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler()),("lr",LogisticRegression(max_iter=1500,class_weight="balanced"))])
    model.fit(tr[FEATS],tr.target);prob=model.predict_proba(te[FEATS])[:,1];pred=(prob>=.5).astype(int)
    metrics={"Accuracy":accuracy_score(te.target,pred),"Balanced accuracy":balanced_accuracy_score(te.target,pred),"Brier score":brier_score_loss(te.target,prob),"Test sessions":len(te)}
    model.fit(train[FEATS],train.target);p=float(model.predict_proba(latest[FEATS])[0,1])
    last=f.dropna(subset=["atr","ema20","ema50","rsi"]).iloc[-1]
    price,atr=float(last.Close),float(last.atr);entry=max(price,float(last.High))+.1*atr
    stop=entry-atr;t1=entry+1.5*atr;t2=entry+2*atr
    trend=price>last.ema20>last.ema50;mom=50<=last.rsi<=72
    if p>=.55 and trend and mom:status="WAIT FOR TRIGGER";why="Bullish model lean plus trend and momentum. Enter only after the trigger is crossed with volume confirmation."
    elif p<=.45:status="NO LONG ENTRY";why="Model currently leans bearish. Do not force a long trade."
    else:status="WAIT / NO TRADE";why="Signals are mixed. Wait for confirmation or skip."
    plan={"price":price,"atr":atr,"entry":entry,"stop":stop,"t1":t1,"t2":t2,"rr":1.5,"trend":trend,"mom":mom,"rsi":float(last.rsi),"status":status,"why":why}
    return d,p,metrics,plan

def freshness_status(last_date):
    """Conservative calendar freshness check for completed daily candles.
    NSE holidays are not embedded; ambiguous dates are flagged for manual review.
    """
    from datetime import datetime, date, time, timedelta
    from zoneinfo import ZoneInfo
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    d = pd.Timestamp(last_date).date()
    today = now.date()
    # During market hours, yesterday's completed candle is expected; after 16:00,
    # today's candle is expected on weekdays. Weekends expect Friday.
    if today.weekday() >= 5:
        expected = today - timedelta(days=today.weekday()-4)
    elif now.time() >= time(16, 0):
        expected = today
    elif now.time() < time(9, 15):
        expected = today - timedelta(days=1 if today.weekday()>0 else 3)
        while expected.weekday() >= 5:
            expected -= timedelta(days=1)
    else:
        expected = today - timedelta(days=1)
        while expected.weekday() >= 5:
            expected -= timedelta(days=1)
    age = (today - d).days
    # A latest candle older than 4 calendar days is definitely too old for this app.
    if age > 4:
        return "STALE", f"Latest candle is {d}; it is {age} calendar days old. Forecast blocked."
    if d < expected:
        return "CHECK", f"Latest candle is {d}; expected approximately {expected}. This may be an exchange holiday or delayed feed. Verify before trading."
    if d > today:
        return "INVALID", f"Provider returned a future candle ({d}); forecast blocked."
    return "FRESH", f"Latest completed daily candle: {d} (India time {now:%d %b %Y, %H:%M})."

def money(x):return f"₹{x:,.2f}"
st.title("📈 NexTrade — Entry & Exit Lab")
st.caption("NSE stock outlook • conditional entry • stop-loss • targets • exit rules")
st.info("Data comes from Yahoo Finance via yfinance (unofficial; may be delayed or incomplete). Each analysis fetches recent market history; daily data is cached for 5 minutes. The app does not run a background job while nobody is using it. After NSE closes, open the app and click Refresh market data, then Analyze stock for the latest available completed candle.")
with st.sidebar:
    st.header("Stock")
    name=st.selectbox("Search 400+ NSE stocks by company name or ticker",list(WATCH), help="Click the box and start typing, e.g. Vedanta, VEDL, Hindustan Unilever, HINDUNILVR, DCM Shriram.")
    custom=st.text_input("Or enter NSE symbol / Yahoo ticker",placeholder="e.g. HINDUNILVR or HINDUNILVR.NS")
    raw_custom=custom.strip().upper().rstrip(".")
    ticker=(raw_custom if raw_custom.endswith(".NS") else raw_custom+".NS") if raw_custom else WATCH[name]
    st.caption("Enter an NSE symbol; .NS is added automatically. Example: HINDUNILVR")
    st.divider();st.write("Plan settings: long-only • stop = 1 ATR • targets = 1.5 ATR and 2 ATR")
tab1,tab2,tab3=st.tabs(["🔎 Analysis & tomorrow","⚡ Intraday entry check","📋 Watchlist scanner"])
with tab1:
    st.subheader(f"{name if not custom else ticker} — next-session outlook")
    c1,c2=st.columns(2)
    go=c1.button("Analyze stock",type="primary",use_container_width=True)
    refresh=c2.button("Refresh market data",use_container_width=True)
    if refresh:daily.clear();intra.clear();st.success("Cached data cleared. Click Analyze stock.")
    if go:
        with st.spinner("Fetching history and testing model…"):
            try:
                d,p,m,pl=analyze(ticker);st.session_state["analysis"]=(ticker,d,p,m,pl)
            except Exception as e:st.error(f"Could not analyze {ticker}: {e}. Check the NSE symbol and try again.")
    if "analysis" in st.session_state and st.session_state["analysis"][0]==ticker:
        _,d,p,m,pl=st.session_state["analysis"]
        freshness, freshness_msg = freshness_status(d.index[-1])
        if freshness == "FRESH":
            st.success("DATA STATUS: FRESH — " + freshness_msg)
        elif freshness == "CHECK":
            st.warning("DATA STATUS: VERIFY — " + freshness_msg + " Do not rely on this forecast until the date is confirmed.")
        else:
            st.error("DATA STATUS: " + freshness + " — " + freshness_msg + " Forecast is blocked.")
        if freshness in ("STALE", "INVALID"):
            st.stop()
        a,b,c=st.columns(3);a.metric("UP probability",f"{p:.1%}");b.metric("DOWN probability",f"{1-p:.1%}");c.metric("Last close",money(float(d.Close.iloc[-1])))
        st.caption(f"Last daily candle: {d.index[-1].date()}")
        if p>=.55:st.success("MODEL LEAN: BULLISH")
        elif p<=.45:st.error("MODEL LEAN: BEARISH")
        else:st.warning("MODEL LEAN: NEUTRAL — weak edge")
        st.markdown("### Conditional entry plan");st.subheader(pl["status"]);st.write(pl["why"])
        a,b,c,dcol=st.columns(4);a.metric("Entry trigger",money(pl["entry"]));b.metric("Stop-loss",money(pl["stop"]));c.metric("Target 1",money(pl["t1"]));dcol.metric("Target 2",money(pl["t2"]))
        st.write(f"Risk/reward to Target 1: **{pl['rr']:.1f}:1** • Trend: **{'Pass' if pl['trend'] else 'Fail'}** • Momentum: **{'Pass' if pl['mom'] else 'Fail'}** (RSI {pl['rsi']:.1f})")
        st.markdown("### Exit rules")
        st.markdown(f"- At **{money(pl['t1'])}**, consider booking part of the position.\n- At **{money(pl['t2'])}**, close the planned trade.\n- At **{money(pl['stop'])}**, exit; never widen the stop to avoid a loss.\n- If price gaps far above entry, do not chase; wait for a retest or skip.\n- If trigger is not crossed, there is **no trade**.")
        st.markdown("### Chronological holdout metrics")
        a,b,c,dcol=st.columns(4);a.metric("Accuracy",f"{m['Accuracy']:.1%}");b.metric("Balanced accuracy",f"{m['Balanced accuracy']:.1%}");c.metric("Brier score",f"{m['Brier score']:.3f}");dcol.metric("Test sessions",m["Test sessions"])
        st.caption("80/20 time-ordered holdout. Not a full strategy backtest; fees, taxes, slippage and gaps are not included.")
        st.markdown("### Recent price");st.line_chart(d.tail(100)[["Close"]])
        st.download_button("Download daily data CSV",d.to_csv().encode(),file_name=f"{ticker.replace('.','_')}.csv")
    else:st.write("Press Analyze stock to fetch history, calculate tomorrow's probability and build the conditional trade plan.")
with tab2:
    st.subheader("Intraday 5-minute confirmation")
    st.write("Checks opening-range breakout, VWAP and relative volume from the latest available 5-minute candles.")
    if st.button("Check intraday setup",type="primary"):
        with st.spinner("Fetching 5-minute data…"):
            try:
                x=intra(ticker)
                if len(x)<25:st.warning("Not enough recent intraday candles. Try during NSE market hours.")
                else:
                    typ=(x.High+x.Low+x.Close)/3;x["VWAP"]=(typ*x.Volume).cumsum()/x.Volume.replace(0,np.nan).cumsum()
                    x["V20"]=x.Volume.rolling(20).mean();day=x[x.index.date==x.index[-1].date()].copy()
                    if len(day)<5:st.warning("Not enough candles in current session.")
                    else:
                        orhigh=float(day.iloc[:3].High.max());last=day.iloc[-1]
                        vwap=float(last.Close)>float(last.VWAP);vol=pd.notna(last.V20) and float(last.Volume)>1.2*float(last.V20);br=float(last.Close)>orhigh
                        st.metric("Latest 5m close",money(float(last.Close)));st.metric("Opening-range high",money(orhigh))
                        st.write(f"Above VWAP: **{'YES' if vwap else 'NO'}** • Volume >1.2× average: **{'YES' if vol else 'NO'}** • Breakout: **{'YES' if br else 'NO'}**")
                        if vwap and vol and br:st.success("All three conditions met. This is a setup alert, not an automatic buy order.")
                        else:st.warning("NO ENTRY YET — wait for all conditions.")
                        st.line_chart(day[["Close","VWAP"]])
            except Exception as e:st.error(f"Intraday data check failed: {e}")
with tab3:
    st.subheader("Scan NSE watchlist")
    st.write("Runs the same next-session model and entry planner for 690 NSE symbols. This can take several minutes and Yahoo may rate-limit large scans.")
    if st.button("Scan all stocks",type="primary"):
        rows=[];bar=st.progress(0);msg=st.empty()
        for i,(n,t) in enumerate(WATCH.items()):
            msg.write(f"Scanning {n} ({i+1}/{len(WATCH)})")
            try:
                d,p,m,pl=analyze(t);rows.append({"Stock":n,"Up probability %":round(p*100,1),"Model view":"Bullish" if p>=.55 else "Bearish" if p<=.45 else "Neutral","Entry status":pl["status"],"Trigger":round(pl["entry"],2),"Stop":round(pl["stop"],2),"Target 1":round(pl["t1"],2),"Holdout accuracy %":round(m["Accuracy"]*100,1)})
            except Exception as e:rows.append({"Stock":n,"Up probability %":np.nan,"Model view":"Unavailable","Entry status":str(e),"Trigger":np.nan,"Stop":np.nan,"Target 1":np.nan,"Holdout accuracy %":np.nan})
            bar.progress((i+1)/len(WATCH))
        msg.empty();st.session_state["scan"]=pd.DataFrame(rows)
    if "scan" in st.session_state:
        st.dataframe(st.session_state["scan"],use_container_width=True,hide_index=True)
        st.download_button("Download scan CSV",st.session_state["scan"].to_csv(index=False).encode(),file_name="nextrade_scan.csv")
st.divider()
st.caption("No order placement. No guaranteed predictions. Forecast probability is not a trade entry. Paper-trade and validate before risking money.")
