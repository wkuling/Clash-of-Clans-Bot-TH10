from datetime import *
from math import *
from random import *
import shutil

cocWindow = App("Bluestacks").window(0)

loons_per_side = 30
minions_per_side = 30

#TODO: check for presence of full army in training
#TODO: remove snow in samples :{

minGoldToAttack = 160000
minElixirToAttack = 160000
minDeToAttack = 0

fullExamples = ["1451644219572.png", "1451663222229.png", "1451713958560.png", "1451714097308.png", "1451714122782.png", "1451714396145.png", "1451714414665.png", "1451738698221.png", "1451764106576.png", "1451766219783.png", "1451766235710.png", "1451766251405.png","1451766260893.png", "1451796406407.png","1451796419942.png","1451796429391.png","1452113488649.png","1452113500761.png","1452113512004.png","1452113551528.png","1452113559922.png","1452144678556.png","1452192239430.png","1452192251064.png","1452192933858.png"]
emptyExamples = ["1451643867528.png", "1451715540614.png", "1451715570452.png","1451715596492.png", "1451715644429.png", "1451715666970.png", "1451715832641.png", "1451715916882.png", "1451716123070.png", "1451738491446.png", "1451738611396.png", "1451765613005.png", "1451826767850.png"]
pumpExamples = ["1456035576329.png", "1456035639369.png"]
#pumpExamples = [ "1451766607360.png","1451766821330.png", "1451766665530.png","1451767058806.png", "1451767126861.png"]
# pumpExamples = ["1451636052190.png", "1451637073330.png", "1451641075253.png", "1451641150949.png"]              


cutX = 175
cutY = 130 
fastSearchArea = Region(cocWindow.x+cutX, cocWindow.y+cutY, cocWindow.w - 2*cutX, cocWindow.h - 2*cutY)

def attack():
    if not startAttacking():
        return False
    for i in range(90): # So, after 90 attacks, return to mainscreen (done through CheckIdle)
        print "Attacks tried ", (i+1)
        sleepytime = randint(0,3)
        sleep(sleepytime)
        if isGoodOpponent():
            if deployTroops():
                finishBattleAndGoHome()
                return True
            else:
                return False
        else:
            if not nextOpponent():
                return False
    return False

def startAttacking():
    try:
        sleep(1)
        cocWindow.find("1453843887137.png").click()
        sleep(1)
        cocWindow.find("1420258681129.png").click()
        sleep(1)
 
        if (cocWindow.exists("1449332295238.png")) or (cocWindow.exists("1420258740243.png")):
            cocWindow.find("1420258740243.png").click()

        return True
    except:
        print "Error starting the attack process"
        return False
        
            

def nextOpponent():
    try:
        cocWindow.find("1420259749784.png").click()
        sleep(2)
        cocWindow.wait("1449332351287.png", 20)
        return True
    except:
        print "Error in searching for new opponent"
        sleep(2)
        return False

def determineTH():
    if (cocWindow.exists("1449930476335.png")):
        temp = cocWindow.getLastMatch()
        return (9, temp.getCenter().getX(), temp.getCenter().getY())
    if (cocWindow.exists("1449930618274.png")):
        temp = cocWindow.getLastMatch()
        return (10, temp.getCenter().getX(), temp.getCenter().getY())
    if (cocWindow.exists("1449930570846.png")):
        temp = cocWindow.getLastMatch()
        return (8, temp.getCenter().getX(), temp.getCenter().getY())
    if (cocWindow.exists("1449930709238.png")):
        temp = cocWindow.getLastMatch()
        return (11, temp.getCenter().getX(), temp.getCenter().getY())
    return False

def allPumpsFull():
    print "Checking Pumps and Vaults now"
    checkshield = False
    checkmine = True
    checktank = False
    checkvault = False
    shieldRegion = Region((cocWindow.x), (cocWindow.y), 67, 141)

# Check for presence of shield
    if (not checkshield) or (shieldRegion.exists(Pattern("1450674720451.png").similar(0.90))):
        if checkshield:
            print "Opponent has no shield"
        else:
            print "Shield not checked"
    else:
        print "Shield found, not a suitable opponent"
        return False

# Check Elixir tanks    
    if (not checktank) or (cocWindow.exists("1450301598264.png")): 
        if checktank:
            print "Found near empty elixir tank level 11"
        else:
            print "Elixir tank not checkend"
    else:
        print "Elixir tank too full, not a suitable opponent"
        return False

# Check Gold vault
    if (not checkvault) or (cocWindow.exists("1450301632194.png")):
        if checkvault:                    
            print "Found near empty gold vault level 11"
        else:
            print "Gold vaults are not checked"
    else:
        print "Gold vault too full, not a suitable opponent"
        return False

# Check goldmine... this is an expensive function in terms of time as it needs to zoom in to determine full goldmines

    if (not checkmine):
        print "Gold mine is not checked"
        return True
    else:
        startTime = datetime.now()
        print "Started pump investigation at: ", str(startTime)
        found = False
        i=0
        matchPump = False
        for pump in pumpExamples:
            if (not found):
                matchPump = fastSearchArea.exists(pump, 1)
                if matchPump and (matchPump.getScore() > 0.75):
                    print "Match with element: ", i
                    allMatchPumps = fastSearchArea.findAll(pump)
                    matchPumpIterator = fastSearchArea.getLastMatches()
                    found = True
                i += 1
        
        if (not found):
            print "No suitable gold mines found" 
            return False
        
        maxIterations = 3
        interimIterations = 2
        iteration = 1
        margin = 0.03
        absoluteMax = 0.95
        absoluteMin = 0.80
        globalFullMineScore = []
        globalEmptyMineScore = []
           
        while matchPumpIterator.hasNext() and iteration <= maxIterations:
            iteration += 1
            pumpArea = Region(matchPumpIterator.next()).nearby(10) 
            # pumpArea.highlight(2)
            matched = False
            matchFull = False
            matchEmpty = False            
            fullMineSimilarityScore = -1                      
            for number, example in enumerate(fullExamples):
                matchFull = pumpArea.exists(example, 0.05)
                if matchFull:
                    if matchFull.getScore() > fullMineSimilarityScore:
                        fullMineSimilarityScore = matchFull.getScore()
                        matched = matchFull
                        print "Iteration: ", iteration
                        print "New best match for full pump on: ", number
                        print "New best score: ", fullMineSimilarityScore
                    else:
                        print "No new best score for number: ", number, "score is: ", matchFull.getScore()
            if matched:
                matched = False
                emptyMineSimilarityScore = -1
                for number, example in enumerate(emptyExamples):
                    matchEmpty = pumpArea.exists(example, 0.05)    
                    if matchEmpty: 
                        if matchEmpty.getScore() > emptyMineSimilarityScore:
                            emptyMineSimilarityScore = matchEmpty.getScore()
                            matched = matchEmpty 
                            print "Iteration: ", iteration
                            print "New best match for empty pump on: ", number
                            print "New best score: ", emptyMineSimilarityScore
                if fullMineSimilarityScore >= 0: globalFullMineScore.append(fullMineSimilarityScore)
                if emptyMineSimilarityScore >= 0: globalEmptyMineScore.append(emptyMineSimilarityScore)

        print globalFullMineScore
        print globalEmptyMineScore


        if (len(globalFullMineScore)>1) or (globalFullMineScore>=absoluteMax):
            fullMineSimilarityScore = mean(globalFullMineScore)
        else:
            print "Too few mines detected (<=1) to accurately assess situation, skipping this village."
            fullMineSimilarityScore = 0       
        if globalEmptyMineScore:
            emptyMineSimilarityScore = mean(globalEmptyMineScore)
        else:
            emptyMineSimilarityScore = 0

        #if abs(fullMineSimilarityScore - emptyMineSimilarityScore) <= 1:
            #img = capture(cocWindow)
            #stamp = str(datetime.now())
            #shutil.move(img, "C:\\Prive\\Learning_examples\\%.5f_%.5f_screenshot.png" % (fullMineSimilarityScore, emptyMineSimilarityScore))
            #print "%s: Saved screenshot for investigation later" %stamp

        print "Median value full: ", median(globalFullMineScore)
        print "Median value empty: ", median(globalEmptyMineScore)
        print
        print "Average value full: ", mean(globalFullMineScore)
        print "Average value empty: ", mean(globalEmptyMineScore)
        print
        print "Safety margin used: ", margin
        endTime = datetime.now()
        print "Function ended at: ", str(endTime)
        print "Processing time: ", str(endTime-startTime)
        print
        if ((fullMineSimilarityScore <= emptyMineSimilarityScore + margin) and (fullMineSimilarityScore <= absoluteMax)) or (fullMineSimilarityScore < absoluteMin):
            print "Gold mine investigated looks more similar to empty gold mine (+ margin score) than full gold mine"
            return False
        else:
            print "Full gold mine detected"

            
# If all conditions are met, it is a suitable opponent
    return True
                        
def isGoodOpponent():
    try:
        goldRegion        =   Region((cocWindow.x + 67), (cocWindow.y + 141), 140, 34)
        elixirRegion      =   Region((cocWindow.x + 67), (cocWindow.y + 180), 140, 34)
        deRegion          =   Region((cocWindow.x + 67), (cocWindow.y + 218), 125, 34)

        gold = numberOCR(goldRegion, 'opponentLootgd')
        elixir = numberOCR(elixirRegion, 'opponentLoote')
        de = numberOCR(deRegion, 'opponentLootde')

        print "Gold, Elixir, Dark: ", gold, elixir, de
        text = "%s,%d,%d,%d\n" % (str(datetime.now()),gold, elixir, de)

        with open('C:\Prive\Sikulilog\Sikulilog.txt', 'a') as f:
            f.write(text)
        if (gold >= minGoldToAttack) and (elixir >= minElixirToAttack) and (de >= minDeToAttack) and allPumpsFull():
            return True
        return False
    except:
        print "isGoodOpponent() Something went wrong :("
        print sys.exc_info()[0]
        print sys.exc_info()[1]
        return False

def deployTroops():
    # TODO: Check for full-ish collectors and deploy troops differently if they exist (around all edges)
    
    print "[+] Deploying troops"
        
    try:

        landmark = cocWindow.find(Pattern("1449812770408.png").similar(0.80))
        
        landmark.highlight(1)
        
        Settings.DelayAfterDrag = 0.1
        Settings.DelayBeforeDrop = 0.3
        Settings.MoveMouseDelay = 0.3
        dragDrop(landmark.getCenter(), Location(cocWindow.x + 68, cocWindow.y + 462))
        Settings.DelayAfterDrag = 0.3
        Settings.DelayAfterDrop = 0.3
        Settings.MoveMouseDelay = 0.3

        landmark = cocWindow.find(Pattern("1449812770408.png").similar(0.80)) # Doing this again to reposition
        landmark.highlight(1)    # Necessary to prevent "flinging" the screen...
        
    except:
        print "[!] Could not find attack landmark. Aborting attack."
        cocWindow.find("1449332433972.png").click()
        return False
        
    deployPoints_loons = []
    deployPoints_minions = []
    print "Landmark x: ", landmark.getX()
    print "Landmark y: ", landmark.getY()

# Derived from original deploypoints. Estimated linear relationship y=f(x)=ax+b  
# Starting with leftunder line

# Order: leftbelow, leftabove, rightbelow, rightabove
    abminmax = [(0.7687, -110.7, 40, 490), (-0.758, -70, 40, 430), (-0.77, 980, 886, 1400), (0.74, -1120, 1025, 1400)]
#    abminmax = [(0.7687, -110.7, 40, 490), (0.7687, -110.7, 40, 490), (-0.77, 980, 886, 1400), (-0.77, 980, 886, 1400)]
    for a, b, xmin, xmax in abminmax:       
        stepsize_loons = floor((xmax-xmin)/float(loons_per_side))
        for x in range(xmin, xmax, stepsize_loons):
            y = ceil(a*x + b)
            deployPoints_loons.append(Location((landmark.getX() + x), (landmark.getY() + y)))
        print "Number of loon deploypoints added: ", len(range(xmin, xmax, stepsize_loons))
        if len(range(xmin, xmax, stepsize_loons)) > loons_per_side: # if accidentally, too many points are added, kill one of them
            deployPoints_loons.pop()
            print "Popped one loon drop point to reduce size"
        if len(range(xmin, xmax, stepsize_loons)) < loons_per_side: # if too few points are added, add one on xmax
            deployPoints_loons.append(Location((landmark.getX() + xmax), (landmark.getY() + a*xmax + b)))
            print "Added one loon drop point to get full deployment"

        stepsize_minions = floor((xmax-xmin)/float(minions_per_side))
        for x in range(xmin, xmax, stepsize_minions):
            y = ceil(a*x + b)
            deployPoints_minions.append(Location((landmark.getX() + x), (landmark.getY() + y)))
        print "Number of minion deploypoints added: ", len(range(xmin, xmax, stepsize_minions))
        if len(range(xmin, xmax, stepsize_minions)) > minions_per_side: # if accidentally, too many points are added, kill one of them
            deployPoints_minions.pop()
            print "Popped one Minion droppoint to reduce size"
        if len(range(xmin, xmax, stepsize_minions)) < minions_per_side: # if too few points are added, add one on xmax
            deployPoints_minions.append(Location((landmark.getX() + xmax), (landmark.getY() + a*xmax + b)))
            print "Added one Minion drop point for full deployment"
    
    Settings.MoveMouseDelay = 0.1

    try:
        # troops_loons     = cocWindow.find("1449911639483.png")
    
        troops_loons = cocWindow.find("1450029597057.png") 
    except:
        troops_loons = False
    
    try:
        # troops_minions        = cocWindow.find("1449911656596.png")
        troops_minions = cocWindow.find("1450029645401.png") 
    except:
        troops_minions = False

   
    try:
        troops_barbking       = cocWindow.find("troops_barbking.png")
    except:
        troops_barbking = False

    try:
        troops_archqueen      = cocWindow.find("1434104532219.png")
    except:
        troops_archqueen = False

    try:
        troops_lightning      = cocWindow.find("1445081986545.png")
    except:
        troops_lightning = False

    print "Starting barch deployment"
    for n in range(4):
        troops_loons.click()
        start = int(n*loons_per_side)
        eind = int(min((n+1)*loons_per_side,len(deployPoints_loons)))
        print start
        print eind
        for point in deployPoints_loons[start:eind]:
            cocWindow.click(point)
        troops_minions.click()
        for point in deployPoints_minions[start:eind]:
            cocWindow.click(point)

#    print "Starting loon deployment" 
#    troops_loons.click()
#    for point in deployPoints_loons:
#        cocWindow.click(point)

#    print "Starting minion deployment"
#    troops_minions.click()
#    for point in deployPoints_minions:
#        cocWindow.click(point)
  
    # Then the Barb King and Archqueen if available
    clickpoint = randint(0, len(deployPoints_minions)) 
    
    if troops_barbking != False:
        troops_barbking.click()
        cocWindow.click(deployPoints_minions[clickpoint])
    if troops_archqueen != False:
        troops_archqueen.click()
        cocWindow.click(deployPoints_minions[clickpoint])
    sleep(8)
    if troops_barbking != False:    
        troops_barbking.click()
    if troops_archqueen != False:
        troops_archqueen.click()

    # Cleanup if necessary
    troops_loons.click()
    for i in range(4*loons_per_side):
        cocWindow.click(deployPoints_minions[clickpoint])
    troops_minions.click()
    for i in range(4*minions_per_side):
        cocWindow.click(deployPoints_minions[clickpoint])
    
    if troops_lightning != False:
        # deRegion = Region((cocWindow.x + 67), (cocWindow.y + 218), 125, 34)
        troops_lightning.click()
        # darknow = numberOCR(deRegion, 'opponentLootde')
        # delta_dark = darknow
        # print "Dark before lightning sequence: ", darknow
        for _ in range(5):
            try:
                #if delta_dark >= 50:
                    #darkold = darknow
                cocWindow.find("1450331436108.png").click()
                    #darknow = numberOCR(deRegion, 'opponentLootde')
                    #delta_dark = darkold - darknow
                    #print "Change in dark due to lightning: ", delta_dark
                sleep(6)
            except:
                pass
             
    print "[+] Troops have all been deployed"

    Settings.MoveMouseDelay = 0.1
    
    return True


def campsFull():
    try:
        output = False
        cocWindow.find("1435988759411.png").click()
        if(cocWindow.exists(Pattern("1449865407262.png").similar(0.93))):
            
            output = True

        cocWindow.find(Pattern("1420240870546.png").similar(0.90)).click()
        return output
    except:
        print "[INFO] Error in checking whether camps are full"
        return False
    
def needToCheck():
    try:
        output = True
        if (cocWindow.find(Pattern("1450506815787.png").similar(0.90))):
            output = False
        return output
    except:
        print "[INFO] Error in checking whether direct training makes sense"
        return True
  
def finishBattleAndGoHome():
    # TODO: Collect (via OCR) stats about the battle
    #       and record them for later analysis and review
    cocWindow.wait("1449349515181.png", 210)
    if (cocWindow.exists("1449349523638.png")):
        cocWindow.getLastMatch().click()
    
        return True
    else:
        return False

def trainTroops():
    # Routine to train troops for attack

    print "[+] Training new troops"
    
    try:
        cocWindow.find("1436077197737.png").click()
        cocWindow.find(Pattern("1434481359875.png").similar(0.95)).click()
        sleep(1)

# Make sure barracks are empty, no remaining 'to be trained groups':
        Settings.MoveMouseDelay = 0.1
        if (cocWindow.exists(Pattern("1449865463693.png").similar(0.93))): 
            cocWindow.find("1420240870546.png").click()
            sleep(2)            
            return True
        
        if needToCheck():
            for i in range (6):
                while (cocWindow.exists(Pattern("1435776186163.png").similar(0.90))):
                    mouseMove(Pattern("1435776186163.png").similar(0.90))
                    mouseDown(Button.LEFT)
                    sleep (3) 
                    mouseUp()
                    sleep (0.5)          
                cocWindow.find(Pattern("1434481359875.png").similar(0.95)).click()
                sleep (1)
            cocWindow.find(Pattern("1449344786371.png").targetOffset(-122,-2)).click()
            sleep(1)
        else:
            print "Camps are empty, no need to check"
        
# Let's train!
        for i in range(4):
            print "clicking loons to be trained"
#            to_click = cocWindow.find("1435776406520.png")

            to_click = cocWindow.find("1450029768897.png")
            to_click2 = cocWindow.find("1450029797031.png")
            for n in range(loons_per_side):
                to_click.click()    
            for n in range(minions_per_side):    
                to_click2.click()            
            cocWindow.find("1420308052116.png").click()
            sleep(1)
#        for i in range(2):
#            print "clicking minions to be trained"
#            to_click = cocWindow.find("1449913483673.png")
#            for n in range(25):
#                to_click.click()
#            cocWindow.find("1420308052116.png").click()
            sleep(1)
            
        # Now, let's train some lightning spells to boost the dark elixir farming with...
        cocWindow.find(Pattern("1449348974233.png").targetOffset(-41,-2)).click()
        sleep(1)
        for n in range(5):
            try:
                cocWindow.find(Pattern("1445081750363.png").similar(0.75)).click()
            except:
                pass
        
        cocWindow.find("1420240870546.png").click()
        
        
        sleep(2)
        
    except:
        print "Error training new troops"
        if cocWindow.exists("1420240870546.png"):
            cocWindow.getLastMatch().click()
        print sys.exc_info()[0]
        print sys.exc_info()[1]




def calcTrainTime(barrack):
    time = 0

    for (i, count) in enumerate(barrack):
        time += (count * trainTimes[i])

    return time

def _openSidebar():
    try:
        if cocWindow.exists("1420308399291.png",0):
            cocWindow.getLastMatch().click()
            sleep(1)
            return True
        else:
            print "Sidebar opener doesn't exist"
            return False
    except:
        print "[!] Could not open sidebar"
        return False



def _closeSidebar():
    try:
        if cocWindow.exists("1420238603713.png", 0):
            cocWindow.getLastMatch().click()
            sleep(2)
            return True
        else:
            print "Sidebar closer doesn't exist"
            return False
    except:
        print "[!] Could not close sidebar"
        return False



def collectResources():
    resources = ["1420235690079.png", "1420231189687.png" ,"1443260705975.png"]

    window = Region((cocWindow.x + 210), (cocWindow.y + 85), 1025, 790)
    window.highlight(3)
    for resource in resources:
        try:
            for _temp in window.findAll(resource):
                _temp.click()
        except:
            print "[!] There was an error collecting resources"
    

    return




# Starts BlueStacks Player
# Opens Clash of Clans app
# Centers village on the screen
#
# Returns: True if succeeded, False if anything failed
def startClashOfClans():
    startAndFocusApp()
    waitVanish("1420181477444.png", FOREVER)
    sleep(3)
    
    cocWindow = App("Bluestacks").window(0)
    recentApps = Region((cocWindow.x + 8), (cocWindow.y + 110), 1430, 150)
    
    try:
        recentApps.find(Pattern("1420182034354.png").exact()).click()
        
        cocWindow.wait("1420182438717.png", 30)
        cocWindow.waitVanish("1420182438717.png", FOREVER)

        if cocWindow.exists("1420255908709.png"):
            cocWindow.getLastMatch().click()
            sleep(1)
        else:
            sleep(3)
        
    except:
        print "[!] Could not find COC icon, assuming game is already started..."

    
    return True


# Zooms the screen all the way out
#
# TODO: Reliably center the village on the map
#
# Returns: True on success, False otherwise
def zoomOutAndCenter():
    try:
        startAndFocusApp()
        print "[+] Zooming out and centering village"
        
        probeRegion = Region((cocWindow.x + 67), (cocWindow.y + 112), 1, 1)
        probeRegion.highlight(1)
        for jj in range(10):
            type("O", Key.CTRL)
            sleep(0.5)  
    except:
        print "[!] Something went wrong while trying to zoom out..."
        return False
    
    return True



def startAndFocusApp():
    try:
        switchApp("C:\Program Files (x86)\BlueStacks\HD-StartLauncher.exe")
        sleep(1)
    except:
        print "[!] Could not start/focus the BlueStacks Player"
        return False
    
    return True



# Checks to see if we've been kicked for being idle
# If so, it will reload the game and reset the village
# so we can pick up where we left off.
#
# TODO: Check for recent attack dialog when we return to from idle
def checkIdle():
    sleepytime = randint(0,3)
    sleep(sleepytime)
    output=False
    if (cocWindow.exists("1434261314820.png")):   
        cocWindow.getLastMatch().click()
        sleep(25)
        output = True        
    if (cocWindow.exists("1451080879815.png")):
        cocWindow.getLastMatch().click()
        sleep(3)
    if (cocWindow.exists("1451081020701.png")):
        cocWindow.getLastMatch().click()
        sleep(3)
    if (cocWindow.exists("1434081589892.png")):
        cocWindow.getLastMatch().click()
        sleep(15)
        output = True        
    
    if (cocWindow.exists("1449912828190.png")):
        cocWindow.getLastMatch().click()
        
        sleep(15)            
        output = True        

    if (cocWindow.exists("1420184095574.png")):
        cocWindow.getLastMatch().click()
        
        sleep(15)            
        output = True        
    if (cocWindow.exists("1435094547913.png")):
        cocWindow.getLastMatch().click()
        sleep(3)
        output = True        
    
    if (cocWindow.exists("1449513899595.png")):
        cocWindow.getLastMatch().click()
        sleep(15)
        output = True        
    
    if (cocWindow.exists("1449349451415.png")):
        cocWindow.getLastMatch().click()
        sleep(15)
        output = True        
    return output

def preventIdle():
# Exception handling is done in main loop
    try:
        _openSidebar()
        sleep(5)
        _closeSidebar()
        sleep(5)
        # collectResources()
    except:
        print "Something didn't work in Preventing Idle..."
        return false


def numberOCR(Reg, ocrType):
    if ocrType == 'opponentLootgd':
        numberImages = [Pattern("1435777897467-1.png").similar(0.95), Pattern("1435777964859-1.png").similar(0.95),Pattern("1435777974432-1.png").similar(0.95),Pattern("1435777991728-1.png").similar(0.95),Pattern("1435778017035-1.png").similar(0.95),Pattern("1435778042241-1.png").similar(0.95),Pattern("1435778076500-1.png").similar(0.95),Pattern("1435778104099-1.png").similar(0.95),Pattern("1435778149456-1.png").similar(0.95),Pattern("1435778172200-1.png").similar(0.95)]
    
    if ocrType == 'opponentLoote':
        numberImages = [Pattern("1435778405976-1.png").similar(0.95),Pattern("1435778430683-1.png").similar(0.95),Pattern("1435778455587-1.png").similar(0.95),Pattern("1435778468876-1.png").similar(0.95),Pattern("1435778476135-1.png").similar(0.95),Pattern("1435778529622-1.png").similar(0.95),Pattern("1435778699082-1.png").similar(0.95),Pattern("1435778722192-1.png").similar(0.95),Pattern("1435778733921-1.png").similar(0.95),Pattern("1435778761846-1.png").similar(0.95)]


    if ocrType == 'opponentLootde':
        numberImages = [Pattern("1444982279904.png").similar(0.95),Pattern("1444982341992.png").similar(0.95),Pattern("1444982352335.png").similar(0.95),Pattern("1444982392822.png").similar(0.95),Pattern("1444982414423.png").similar(0.95),Pattern("1444982632547.png").similar(0.95),Pattern("1444982688939.png").similar(0.95),Pattern("1444982718187.png").similar(0.95),Pattern("1444982763458.png").similar(0.95),Pattern("1444982782354.png").similar(0.95)]
        
    digitalNumber = 0
    resultList = list()
    # Reg.highlight(3)
    
    for x in numberImages:
        if Reg.exists(x,0):
            Reg.findAll(x)
            #digital find result into list            
            digitalList = list(Reg.getLastMatches())
            #convert list into tuple(image, digital)
            for y in digitalList:
                #resultList.append(tuple(y,0))
                t = (y,digitalNumber)
                resultList.append(t)
        digitalNumber = digitalNumber+1
    sortedResultList = sorted(resultList,key=lambda x: x[0].x)
    #print sortedResultList
    ret = 0
    listLen = len(sortedResultList)
    for x, i in enumerate(sortedResultList):
        ret += 10 **(listLen - x - 1) * i[1]   
    return ret

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def mean(lst):
    if len(lst) > 0:
        return sum(lst) / float(len(lst))
    else:
        return 0

def secondsSinceLast(ts):
    diff = datetime.now() - ts;

    return diff.seconds

def initialise():
    print "[INFO] RESTART at: " + str(datetime.now()) 
    startAndFocusApp()
    checkIdle()
    print "[INFO] Ready to go at: " + str(datetime.now())


def attackLoop():
    try:
        checkIdle()
        zoomOutAndCenter()
        if (campsFull() == True):                     
            print "[INFO] Time to clean up, train and then attack..."
            trainTroops()
            zoomOutAndCenter()
            attack()
        else:            
            preventIdle()
    except:
        print "[INFO] Error with Bluestacks player detected at: " + str(datetime.now())
        initialise()
    
# Main 'program' HAHA

# Uncomment to debug allPumpsFull() function

#allPumpsFull()

initialise()
while True:
    attackLoop()
 