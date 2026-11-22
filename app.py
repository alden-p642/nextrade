import streamlit as st, yfinance as yf, pandas as pd, numpy as np, warnings, re, os, io
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss
warnings.filterwarnings("ignore")
st.set_page_config(page_title="NexTrade — Equity & Futures Lab", page_icon="📈", layout="wide")
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

def directional_futures_proxy(ticker):
    """Directional LONG/SHORT research using the underlying cash-equity series.
    This is NOT a futures-contract price forecast.
    """
    d, p, metrics, _ = analyze(ticker)
    f = features(d)
    last = f.dropna(subset=["atr", "ema20", "ema50", "rsi"]).iloc[-1]
    price, atr = float(last.Close), float(last.atr)
    up_trend = price > float(last.ema20) > float(last.ema50)
    down_trend = price < float(last.ema20) < float(last.ema50)
    up_momentum = 50 <= float(last.rsi) <= 72
    down_momentum = 28 <= float(last.rsi) <= 50

    if p >= .55 and up_trend and up_momentum:
        direction = "LONG"
        trigger = max(price, float(last.High)) + .1 * atr
        stop = trigger - atr
        target1, target2 = trigger + 1.5 * atr, trigger + 2 * atr
        status = "LONG SETUP — WAIT FOR TRIGGER"
        reason = "Upward model lean, bullish EMA alignment and supportive RSI. This is a conditional setup, not an instruction to enter immediately."
    elif p <= .45 and down_trend and down_momentum:
        direction = "SHORT"
        trigger = min(price, float(last.Low)) - .1 * atr
        stop = trigger + atr
        target1, target2 = trigger - 1.5 * atr, trigger - 2 * atr
        status = "SHORT SETUP — WAIT FOR TRIGGER"
        reason = "Downward model lean, bearish EMA alignment and supportive downside momentum. This is a conditional setup, not an instruction to enter immediately."
    else:
        direction = "WAIT"
        trigger = stop = target1 = target2 = np.nan
        status = "WAIT / NO TRADE"
        failed = []
        if p > .45 and not up_trend: failed.append("bullish trend")
        if p < .55 and not down_trend: failed.append("bearish trend")
        if p >= .55 and not up_momentum: failed.append("bullish RSI momentum")
        if p <= .45 and not down_momentum: failed.append("bearish RSI momentum")
        reason = "The model and confirmation rules do not align" + (": " + ", ".join(failed) if failed else "") + ". Avoid forcing a position."
    return d, p, metrics, {
        "direction": direction, "price": price, "atr": atr, "entry": trigger,
        "stop": stop, "t1": target1, "t2": target2, "status": status,
        "why": reason, "up_trend": up_trend, "down_trend": down_trend,
        "rsi": float(last.rsi)
    }


def parse_nse_futures_contract_file(uploaded_file):
    """Read NSE UDiFF F&O contract CSV/CSV.GZ and return active individual stock futures."""
    import io
    raw = uploaded_file.getvalue()
    name = uploaded_file.name.lower()
    compression = "gzip" if name.endswith(".gz") else "infer"
    frame = pd.read_csv(io.BytesIO(raw), compression=compression, low_memory=False)
    frame.columns = [str(c).strip() for c in frame.columns]
    normalized = {re.sub(r"[^a-z0-9]", "", c.lower()): c for c in frame.columns}

    def pick(*aliases):
        for alias in aliases:
            key = re.sub(r"[^a-z0-9]", "", alias.lower())
            if key in normalized:
                return normalized[key]
        return None

    # Current NSE MII contract file uses FinInstrmNm=FUTSTK, TckrSymb,
    # XpryDt (seconds since 1980-01-01), and NewBrdLotQty.
    sym_col = pick("TckrSymb", "SYMBOL", "Ticker Symbol", "Underlying Symbol")
    inst_col = pick("FinInstrmNm", "INSTRUMENT", "Instrument Type", "InstType", "FinInstrmTp")
    exp_col = pick("XpryDt", "EXPIRY_DT", "Expiry Date", "Expiry")
    lot_col = pick("NewBrdLotQty", "LOT_SIZE", "Lot Size", "Market Lot", "MinLot")
    if not all([sym_col, inst_col, exp_col]):
        raise ValueError(
            "This file's columns were not recognised. Expected NSE fields such as "
            "FinInstrmNm, TckrSymb and XpryDt. Please upload the F&O-MII contract file."
        )

    out = frame[[sym_col, inst_col, exp_col] + ([lot_col] if lot_col else [])].copy()
    out.columns = ["Symbol", "Instrument", "Expiry"] + (["Lot size"] if lot_col else [])
    out["Symbol"] = out["Symbol"].astype(str).str.strip().str.upper()
    out["Instrument"] = out["Instrument"].astype(str).str.strip().str.upper()
    out = out[out["Instrument"].eq("FUTSTK")].copy()
    # NSE MII master timestamps count seconds from 1980-01-01, not
    # the Unix epoch (1970-01-01). Using the wrong epoch shifts dates by 10 years.
    exp_numeric = pd.to_numeric(out["Expiry"], errors="coerce")
    if exp_numeric.notna().mean() > 0.8:
        nse_epoch = pd.Timestamp("1980-01-01", tz="UTC")
        out["Expiry"] = (nse_epoch + pd.to_timedelta(exp_numeric, unit="s", errors="coerce")).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
    else:
        out["Expiry"] = pd.to_datetime(out["Expiry"], errors="coerce", dayfirst=True)
    if "Lot size" in out:
        out["Lot size"] = pd.to_numeric(out["Lot size"], errors="coerce")
    out = out.dropna(subset=["Expiry"])
    # Ignore NSE test instruments and contracts that have already expired.
    out = out[~out["Symbol"].str.endswith("NSETEST", na=False)]
    today = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize()
    out = out[out["Expiry"] >= today]
    out = out.sort_values(["Symbol", "Expiry"]).drop_duplicates(["Symbol", "Expiry"])
    if out.empty:
        raise ValueError(
            "NSE format recognised (FUTSTK), but no unexpired individual stock-futures "
            "contracts were found after applying NSE's 1980-based expiry timestamp. "
            "Please check that the uploaded contract file is the latest NSE F&O-MII file."
        )
    return out.reset_index(drop=True)


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

def load_gift_history(uploaded=None):
    """Load normalized GIFT Nifty daily OHLC history from repo CSV and optional upload."""
    frames=[]
    archive=os.path.join(os.path.dirname(__file__), "data", "gift_nifty_history.csv")
    if os.path.exists(archive):
        try:
            frames.append(pd.read_csv(archive))
        except Exception:
            pass
    if uploaded is not None:
        try:
            frames.append(pd.read_csv(uploaded))
        except Exception as exc:
            raise ValueError(f"Could not read GIFT Nifty CSV: {exc}")
    if not frames:
        return pd.DataFrame()
    raw=pd.concat(frames, ignore_index=True)
    raw.columns=[str(c).strip() for c in raw.columns]
    norm={re.sub(r"[^a-z0-9]", "", c.lower()):c for c in raw.columns}
    def find(*names):
        for n in names:
            k=re.sub(r"[^a-z0-9]", "", n.lower())
            if k in norm:return norm[k]
        return None
    dc=find("Date","Trade Date","Trading Date","BizDt")
    cc=find("Close","Close Price","ClsPric","Settlement Price","SettlPrice")
    if not dc or not cc:
        raise ValueError("CSV must contain Date and Close columns. Optional columns: Open, High, Low, Volume.")
    out=pd.DataFrame()
    out["Date"]=pd.to_datetime(raw[dc], errors="coerce", dayfirst=True)
    for target, aliases in {
        "Open":("Open","Open Price","OpnPric"),
        "High":("High","High Price","HghPric"),
        "Low":("Low","Low Price","LwPric"),
        "Close":("Close","Close Price","ClsPric","Settlement Price","SettlPrice"),
        "Volume":("Volume","Traded Quantity","TtlTradgVol")
    }.items():
        col=find(*aliases)
        out[target]=pd.to_numeric(raw[col],errors="coerce") if col else (out["Close"] if target in ("Open","High","Low") and "Close" in out else np.nan)
    out=out.dropna(subset=["Date","Close"]).sort_values("Date").drop_duplicates("Date",keep="last").set_index("Date")
    if out.empty: raise ValueError("No valid dated GIFT Nifty rows were found in the CSV.")
    out["Change points"]=out["Close"].diff()
    out["Change %"]=out["Close"].pct_change()*100
    return out

def gift_market_context(history):
    """Simple context overlay; does not alter the stock model probability."""
    if history is None or len(history)<2:
        return "UNAVAILABLE", np.nan, np.nan
    last=history.iloc[-1]
    chg=float(last["Change %"]); pts=float(last["Change points"])
    if chg>=0.35: view="BULLISH"
    elif chg<=-0.35: view="BEARISH"
    else: view="NEUTRAL"
    return view,pts,chg

st.title("📈 NexTrade — Equity & Futures Lab")
st.caption("NSE equity analysis • stock-futures directional research • conditional levels • risk controls")
st.info("Data comes from Yahoo Finance via yfinance (unofficial; may be delayed or incomplete). Each analysis fetches recent market history; daily data is cached for 5 minutes. The app does not run a background job while nobody is using it. After NSE closes, open the app and click Refresh market data, then Analyze stock for the latest available completed candle.")
with st.sidebar:
    st.header("Stock")
    name=st.selectbox("Search 400+ NSE stocks by company name or ticker",list(WATCH), help="Click the box and start typing, e.g. Vedanta, VEDL, Hindustan Unilever, HINDUNILVR, DCM Shriram.")
    custom=st.text_input("Or enter NSE symbol / Yahoo ticker",placeholder="e.g. HINDUNILVR or HINDUNILVR.NS")
    raw_custom=custom.strip().upper().rstrip(".")
    ticker=(raw_custom if raw_custom.endswith(".NS") else raw_custom+".NS") if raw_custom else WATCH[name]
    st.caption("Enter an NSE symbol; .NS is added automatically. Example: HINDUNILVR")
    st.divider();st.write("Plan settings: long-only • stop = 1 ATR • targets = 1.5 ATR and 2 ATR")
tab1,tab2,tab3,tab4,tab5=st.tabs(["🔎 Analysis & tomorrow","⚡ Intraday entry check","📋 Watchlist scanner","📉 Futures LONG / SHORT","🌍 GIFT Nifty pulse"])
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
        gift_hist=load_gift_history()
        gift_view,gift_pts,gift_pct=gift_market_context(gift_hist)
        st.markdown("### GIFT Nifty global-market confirmation")
        if gift_view != "UNAVAILABLE":
            st.write(f"Latest archived GIFT Nifty session: **{gift_hist.index[-1].date()}** • Daily move: **{gift_pts:+,.2f} points ({gift_pct:+.2f}%)** • Context: **{gift_view}**")
            if pl["status"].startswith("LONG") and gift_view=="BEARISH": st.warning("GIFT Nifty is negative: this LONG setup is against the global-market context. Treat it as lower-conviction and wait for stronger confirmation.")
            elif pl["status"].startswith("SHORT") and gift_view=="BULLISH": st.warning("GIFT Nifty is positive: this SHORT setup is against the global-market context. Treat it as lower-conviction and wait for stronger confirmation.")
            elif (pl["status"].startswith("LONG") and gift_view=="BULLISH") or (pl["status"].startswith("SHORT") and gift_view=="BEARISH"):
                st.success("GIFT Nifty direction agrees with this setup. This is supporting context, not a guarantee.")
            else: st.info("GIFT Nifty is neutral or the stock setup is not directional; it adds no confirmation today.")
        else:
            st.info("No GIFT Nifty history archive yet. Add a daily GIFT Nifty OHLC CSV in the GIFT Nifty pulse tab to activate this context check.")
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

with tab4:
    st.subheader("NSE individual stock futures — directional research")
    st.warning(
        "Important data limitation: the prediction below uses the underlying NSE cash-share history from Yahoo Finance as a proxy. "
        "It does NOT forecast the actual futures contract price, basis, open interest or intraday futures order flow. "
        "Use it for research/paper-trading only until a reliable historical futures data feed is connected."
    )
    st.markdown(
        "NexTrade now checks the repository's automatically refreshed NSE files first. "
        "A scheduled GitHub Actions workflow downloads the latest contract master and UDiFF bhavcopy on trading days. "
        "Manual upload remains available only as a fallback if the automatic refresh has not succeeded."
    )
    st.caption("Official NSE reports: https://www.nseindia.com/all-reports-derivatives")
    status_path = os.path.join(os.path.dirname(__file__), "data", "nse_futures_data_status.json")
    auto_contract_path = os.path.join(os.path.dirname(__file__), "data", "latest_nse_fo_contract.csv.gz")
    auto_bhavcopy_path = os.path.join(os.path.dirname(__file__), "data", "latest_nse_fo_bhavcopy.csv.zip")
    auto_contract_date = None
    if os.path.exists(status_path):
        try:
            import json
            with open(status_path, "r", encoding="utf-8") as status_in:
                daily_status = json.load(status_in)
            # The downloader stores the shared trading-session date at the
            # top level as data_date. Use per-file dates when available, and
            # fall back to data_date for the current status-file format.
            market_date = daily_status.get("data_date") or "date unavailable"
            contract_info = daily_status.get("contract_master") or {}
            bhavcopy_info = daily_status.get("udiff_bhavcopy") or {}
            auto_contract_date = contract_info.get("date") or market_date
            auto_bhavcopy_date = bhavcopy_info.get("date") or market_date

            st.success(
                f"Automatic NSE refresh available — contract master: {auto_contract_date}; "
                f"UDiFF bhavcopy: {auto_bhavcopy_date}"
            )
            st.caption("Last downloader run (UTC): " + daily_status.get("updated_at_utc", "unknown"))
        except Exception as status_error:
            st.warning(f"Could not read NSE refresh status: {status_error}")
    else:
        st.warning("No automatic NSE refresh has been committed yet. GitHub Actions must complete its first run.")

    contract_file = st.file_uploader(
        "Optional fallback: upload an NSE F&O contract file (.csv or .csv.gz)",
        type=["csv", "gz"],
        key="nse_futures_contract_file"
    )
    # Keep the last uploaded contract master on the Streamlit server so a new
    # browser session can reuse it without asking the user to upload again.
    # Streamlit-hosted filesystems are ephemeral, so a server restart/redeploy
    # may clear this cache; the user can upload a fresh master at any time.
    contract_cache_path = "/tmp/nextrade_nse_futures_contract_cache.csv.gz"
    contract_source = None
    if os.path.exists(auto_contract_path) and contract_file is None:
        try:
            with open(auto_contract_path, "rb") as auto_in:
                auto_bytes = auto_in.read()
            contract_source = io.BytesIO(auto_bytes)
            contract_source.name = "latest_nse_fo_contract.csv.gz"
            st.caption("Using the automatically downloaded NSE contract master — no manual upload needed.")
        except Exception as auto_error:
            st.warning(f"Could not read automatic NSE contract file: {auto_error}")
    if contract_file is not None:
        try:
            with open(contract_cache_path, "wb") as cache_out:
                cache_out.write(contract_file.getvalue())
            contract_source = contract_file
            st.caption("Latest uploaded NSE contract file saved in the app's server cache for future visits to this running app.")
        except Exception as cache_error:
            st.warning(f"Could not save the uploaded contract file for reuse: {cache_error}")
            contract_source = contract_file
    elif contract_source is None and os.path.exists(contract_cache_path):
        try:
            with open(contract_cache_path, "rb") as cache_in:
                cached_bytes = cache_in.read()
            contract_source = io.BytesIO(cached_bytes)
            contract_source.name = "saved_nse_futures_contract.csv.gz"
            st.success("Using your previously uploaded NSE contract file — no re-upload needed.")
        except Exception as cache_error:
            st.warning(f"Could not load the saved contract file: {cache_error}")

    if contract_source is not None:
        try:
            contracts = parse_nse_futures_contract_file(contract_source)
            st.success(f"Loaded {contracts['Symbol'].nunique()} stock-futures underlyings and {len(contracts)} expiry contracts.")
            symbols = sorted(contracts["Symbol"].unique().tolist())
            chosen_symbol = st.selectbox("Search stock futures underlying", symbols, key="futures_underlying")
            available = contracts[contracts["Symbol"] == chosen_symbol].sort_values("Expiry")
            expiry_labels = {
                f"{row.Expiry:%d %b %Y}" + (f" — lot {int(row['Lot size'])}" if pd.notna(row.get("Lot size", np.nan)) else ""): row
                for _, row in available.iterrows()
            }
            selected_label = st.selectbox("Select contract expiry", list(expiry_labels), key="futures_expiry")
            selected_contract = expiry_labels[selected_label]
            lot_size = selected_contract.get("Lot size", np.nan)
            a, b, c = st.columns(3)
            a.metric("Underlying", chosen_symbol)
            b.metric("Expiry", selected_contract.Expiry.strftime("%d %b %Y"))
            c.metric("Lot size", str(int(lot_size)) if pd.notna(lot_size) else "Not in file")
            st.caption("The selected expiry/lot are contract metadata only. The directional model below still uses the underlying cash-share price series.")
            if st.button("Analyze futures direction", type="primary", key="analyze_futures"):
                with st.spinner("Training directional model on underlying daily history…"):
                    try:
                        fticker = chosen_symbol + ".NS"
                        fd, fp, fm, fpl = directional_futures_proxy(fticker)
                        st.session_state["futures_analysis"] = (chosen_symbol, selected_contract.Expiry, fd, fp, fm, fpl, lot_size)
                    except Exception as e:
                        st.error(f"Could not analyze {chosen_symbol}: {e}")
            if "futures_analysis" in st.session_state:
                fsym, fexp, fd, fp, fm, fpl, flot = st.session_state["futures_analysis"]
                if fsym == chosen_symbol and pd.Timestamp(fexp) == pd.Timestamp(selected_contract.Expiry):
                    freshness, freshness_msg = freshness_status(fd.index[-1])
                    if freshness == "FRESH":
                        st.success("UNDERLYING DATA: FRESH — " + freshness_msg)
                    elif freshness == "CHECK":
                        st.warning("UNDERLYING DATA: VERIFY — " + freshness_msg)
                    else:
                        st.error("UNDERLYING DATA: " + freshness + " — " + freshness_msg)
                    st.caption(f"Last underlying cash-market candle: {fd.index[-1].date()}")
                    left, right, third = st.columns(3)
                    left.metric("Up probability", f"{fp:.1%}")
                    right.metric("Down probability", f"{1-fp:.1%}")
                    third.metric("Underlying last close", money(float(fd.Close.iloc[-1])))
                    if fpl["direction"] == "LONG":
                        st.success("MODEL DIRECTION: LONG")
                    elif fpl["direction"] == "SHORT":
                        st.error("MODEL DIRECTION: SHORT")
                    else:
                        st.warning("MODEL DIRECTION: WAIT / NO TRADE")
                    st.subheader(fpl["status"])
                    st.write(fpl["why"])
                    gift_hist=load_gift_history()
                    gift_view,gift_pts,gift_pct=gift_market_context(gift_hist)
                    if gift_view != "UNAVAILABLE":
                        st.write(f"GIFT Nifty context ({gift_hist.index[-1].date()}): **{gift_view}** • **{gift_pts:+,.2f} points ({gift_pct:+.2f}%)**")
                        if fpl["direction"]=="LONG" and gift_view=="BEARISH": st.warning("Countertrend warning: GIFT Nifty is negative. Wait for additional confirmation.")
                        elif fpl["direction"]=="SHORT" and gift_view=="BULLISH": st.warning("Countertrend warning: GIFT Nifty is positive. Wait for additional confirmation.")
                        elif (fpl["direction"]=="LONG" and gift_view=="BULLISH") or (fpl["direction"]=="SHORT" and gift_view=="BEARISH"): st.success("GIFT Nifty direction supports this setup; it does not guarantee follow-through.")
                    if fpl["direction"] in ("LONG", "SHORT"):
                        a, b, c, dcol = st.columns(4)
                        a.metric("Underlying trigger", money(fpl["entry"]))
                        b.metric("Underlying stop", money(fpl["stop"]))
                        c.metric("Underlying target 1", money(fpl["t1"]))
                        dcol.metric("Underlying target 2", money(fpl["t2"]))
                        st.caption("These levels are calculated from the underlying cash-share ATR, not the futures contract. Do not transfer them directly to a futures order.")
                    st.write(
                        f"Trend: **{'Bullish' if fpl['up_trend'] else 'Bearish' if fpl['down_trend'] else 'Mixed'}** "
                        f"• RSI: **{fpl['rsi']:.1f}** • Holdout balanced accuracy: **{fm['Balanced accuracy']:.1%}**"
                    )
                    st.line_chart(fd.tail(100)[["Close"]])
                    st.download_button(
                        "Download underlying history CSV",
                        fd.to_csv().encode(),
                        file_name=f"{fsym}_underlying_history.csv",
                        key="download_futures_proxy"
                    )
                    st.caption("The displayed holdout metrics evaluate next-day direction on the underlying share, not a futures trading strategy. They do not include leverage, margin, rollover, brokerage, taxes, slippage or gap risk.")
        except Exception as e:
            st.error(f"Could not read this contract file: {e}")
    else:
        st.info("No NSE contract file is available yet. Check the GitHub Actions workflow named 'Update NSE futures data'. If its first run failed, you can temporarily use the optional manual upload above.")

with tab5:
    st.subheader("GIFT Nifty — global-market pulse")
    st.write("Track daily GIFT Nifty futures OHLC, measure the daily points and percentage move, and use the latest archived session as a confirmation overlay for Indian-stock analysis.")
    st.info("Data integrity note: this version accepts a normalized daily CSV. It does not pretend that NSE Nifty spot data is GIFT Nifty, and it does not yet auto-download NSE IX bhavcopy files. The official NSE IX reports page lists separate Session 1 and Session 2 futures bhavcopies; the report download format must be validated before automatic ingestion is enabled.")
    st.markdown("Official source: https://www.nseix.com/markets/reports")
    gift_upload=st.file_uploader("Upload GIFT Nifty daily history CSV",type=["csv"],key="gift_nifty_csv")
    try:
        gh=load_gift_history(gift_upload)
        if not gh.empty:
            latest=gh.iloc[-1]
            a,b,c=st.columns(3)
            a.metric("Latest close",f"{latest['Close']:,.2f}")
            b.metric("Daily move",f"{latest['Change points']:+,.2f} points" if pd.notna(latest['Change points']) else "—")
            c.metric("Daily change",f"{latest['Change %']:+.2f}%" if pd.notna(latest['Change %']) else "—")
            st.caption(f"Latest archived session: {gh.index[-1].date()} • Sessions stored: {len(gh)}")
            st.line_chart(gh[["Close"]].tail(180),height=300)
            if all(col in gh for col in ["Open","High","Low","Close"]):
                st.subheader("Daily OHLC history")
                st.dataframe(gh.tail(30).sort_index(ascending=False),use_container_width=True)
            view,pts,pct=gift_market_context(gh)
            st.write(f"Current context classification: **{view}** (±0.35% daily threshold; configurable in a later calibration step).")
            st.download_button("Download normalized GIFT Nifty archive CSV",gh.to_csv().encode("utf-8"),file_name="gift_nifty_history.csv",key="gift_archive_download")
            if gift_upload is not None:
                st.warning("This uploaded history is available for this app session and can be downloaded as a normalized archive. To make it persistent across deployments, place the downloaded gift_nifty_history.csv in the repository's data/ folder and commit it to GitHub.")
        else:
            st.warning("No GIFT Nifty history is stored yet. Upload a CSV containing at least Date and Close; Open, High, Low and Volume are recommended.")
    except Exception as gift_error:
        st.error(f"GIFT Nifty data could not be loaded: {gift_error}")
    st.markdown("**Expected CSV columns**")
    st.code("Date,Open,High,Low,Close,Volume\n2026-11-20,....,....,....,....,....",language="csv")
    st.caption("The GIFT overlay only adds market-context warnings/confirmation. It does not change the underlying stock model's probability or automatically create LONG/SHORT trades. Historical validation is required before increasing its influence.")

st.divider()
st.caption("No order placement. No guaranteed predictions. Forecast probability is not a trade entry. Paper-trade and validate before risking money.")
