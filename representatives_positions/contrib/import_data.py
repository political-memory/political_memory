# coding: utf-8
# flake8: noqa

# This dict is used to find dates from URLs for dateless positions
position_dates = {
	"http://www.dailymotion.com/video/x8pi7a_marielle-de-sarnez-l-europe-et-les_news#from=embed&start=1": "2009-03-18",
	"http://tempsreel.nouvelobs.com/election-presidentielle-2012/20111215.OBS6873/interview-eva-joly-legalisons-le-partage-sur-internet.html": "2011-12-17",
	"http://patricklehyaricpe.wordpress.com/2010/03/10/le-parlement-eurpeen-a-battu-swift-il-doit-battre-acta/": "2010-03-10",
	"http://www.sanchezschmid.eu/uploads/PDF/lettre-MT2S-1Trim.pdf": "2010-01-01",
	"http://www.tokia-saifi.eu/index.php?option=com_content&view=article&id=201:halte-a-la-contrefacon-et-au-piratage&catid=65:commerce-international&Itemid=96&lang=fr": "2010-01-01",
	"http://www.tokia-saifi.eu/index.php?option=com_content&view=article&id=283%3Ale-piratage-en-ligne-reprime-&catid=34%3Aactualites&lang=fr": "2010-01-01",
	"http://www.tokia-saifi.eu/index.php?option=com_content&view=article&id=296%3Alacta-un-bouclier-protecteur-pour-lindustrie-europeenne-&catid=34%3Aactualites&lang=fr": "2010-01-01",
	"http://www.tokia-saifi.eu/index.php?option=com_content&view=article&id=230%3Aqlacta-un-accord-commercial-international-essentiel-pour-lutter-contre-la-contrefacon-a-lechelle-internationaleq-tokia-saifi-ump-ppe-f&catid=35%3Ainterventions-en-seance-pleniere&Itemid=59&lang=fr": "2010-01-01",
	"http://www.marietjeschaake.eu/12/05/2011/une-%C2%AB-diplomatie-culturelle-%C2%BB-pour-promouvoir-les-valeurs-europeennes-2/?lang=fr": "2011-05-12",
	"http://www.eurocitoyenne.fr/content/acta-un-rejet-de-cet-accord-par-le-parlement-europeen-est-possible-sil-y-une-mobilisation-co": "2010-01-01",
	"http://www.eurocitoyenne.fr/content/arretons-la-piraterie-en-public": "2010-01-01",
	"http://www.eurocitoyenne.fr/content/le-guide-juridique-la-protection-des-donnees-personnelles-sans-vie-privee-pas-de-liberte": "2010-01-01",
}

# This dict maps full names from old memopol to [1st, last] names in new memopol
# Necessary because we sometimes have different accents/hyphenation/separation, or additional/missing name parts.
rep_names = {
	u"Alexander Graf LAMBSDORFF": [u"Alexander Graf", u"Graf LAMBSDORFF"],
	u"Carlos José ITURGAIZ ANGULO": [u"Carlos", u"ITURGAIZ"],

	u"Cristian Silviu BUŞOI": [u"Cristian-Silviu", u"BUŞOI"],
	u"Eider GARDIAZÁBAL RUBIAL": [u"Eider", u"GARDIAZABAL RUBIAL"],
	u"Filiz Hakaeva HYUSMENOVA": [u"Filiz", u"HYUSMENOVA"],
	u"Glenis WILLMOTT": [u"Dame Glenis", u"WILLMOTT"],
	u"Iliana Malinova IOTOVA": [u"Iliana", u"IOTOVA"],
	u"Janusz Władysław ZEMKE": [u"Janusz", u"ZEMKE"],
	u"Marielle de SARNEZ": [u"Marielle", u"de SARNEZ"],
	u"Monica Luisa MACOVEI": [u"Monica", u"MACOVEI"],
	u"Róża Gräfin von THUN UND HOHENSTEIN": [u"Róża Gräfin", u"von THUN UND HOHENSTEIN"],
	u"Santiago FISAS AYXELA": [u"Santiago", u"FISAS AYXELÀ"],
	u"Sophia in 't VELD": [u"Sophia", u"in 't VELD"],
	u"Vasilica Viorica DĂNCILĂ": [u"Viorica", u"DĂNCILĂ"],
	u"Wim van de CAMP": [u"Wim", u"van de CAMP"]
}
