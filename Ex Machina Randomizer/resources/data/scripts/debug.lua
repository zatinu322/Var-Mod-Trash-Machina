-- Debug shit
-- $Id: debug.lua,v 1.40 2005/07/06 12:55:55 anton Exp $

-------------------------------------------------
-- some debug shit, remove it before release
-------------------------------------------------

function testLoadSave()
	RuleConsole "save test1"
	RuleConsole "load test1"
	RuleConsole "save test2"
end

-- Just for bugfixing
function SetPositionNull()
	GetPlayerVehicle():SetPosition(nil)
end

-------------------------------
-- some function for camera log
function p()
    local pos, rot, lookAt = GetCameraPos()
    LOG(' <Point  coord="' .. strsub( tostring(pos), 2, strlen( tostring(pos) ) - 1 ) .. '" rotation="'.. strsub( tostring(rot), 2, strlen( tostring(rot) ) - 1 ) .. '"/>')
end


function c()
    logCameraPos()
end


------------------------------
--Player pos to log
function plp()
LOG("SetPosition( CVector"..tostring(GetPlayerVehicle():GetPosition())..")")
LOG(' SetRotation(Quaternion'..tostring(GetPlayerVehicle():GetRotation(Quaternion()))..')')
end


-- writes current camera position and angles to log
function logPoint()
	local pos, rot, lookAt = GetCameraPos()
	local sPos = tostring(pos)
	sPos = strsub( sPos, 2, strlen(sPos) - 1 )
	local sRot = tostring(rot)
	sRot = strsub( sRot, 2, strlen(sRot) - 1 )
	LOG( "		<Point")
	LOG( '			coord="'.. sPos ..'"' )
	LOG( '			rotation="'.. sRot .. '"/>' )
end

-- writes current camera position and angles to log
function logPointS()
	local pos, rot, lookAt = GetCameraPos()
	local sPos = tostring(pos)
	sPos = strsub( sPos, 2, strlen(sPos) - 1 )
	local sRot = tostring(rot)
	sRot = strsub( sRot, 2, strlen(sRot) - 1 )
	writeln( "		<Point")
	writeln( '			coord="'.. sPos ..'"' )
	writeln( '			rotation="'.. sRot .. '"/>' )
end

-----------------------
-- create army (cheat!)

-- debug creation of objects in Player position
function DebugCreate( PrototypeName, Belong )
	local id = CreateNewObject{
		prototypeName = PrototypeName,
		objName = "debug_object"..tostring(random(9999)),
		belong = Belong
	}

	local obj = GetEntityByID( id )

	println( "Object created. id = "..tostring(id) )
end


function CreateVehicleEx( PrototypeName, Name, pos, belong )
	local bel
	local rand_vehex = 0
	local rand_guns = 0

	if belong then
		bel = belong
	else
		bel = 1100
	end

	if rand_vehex == 1 then
		PrototypeName = prot_random(1, "ex")
	end

	local id = CreateNewObject {
		prototypeName = PrototypeName,
		objName = Name,
		belong = bel
	}

	local vehicle = GetEntityByID( id )
	
	if not vehicle then
		println( "Error: vehicle ".. PrototypeName .. " not created" )
		return nil
	end

--	by Anton: это не нужно, т.к. вызываем SetGamePositionOnGround()
--	local hover = 1.5 * vehicle:GetSize().y
--	pos.y = g_ObjCont:GetHeight( pos.x, pos.z ) + hover


	vehicle:SetGamePositionOnGround( pos )

	if rand_guns == 1 then
		giveguns(Name)
	end

	return vehicle
end

function prot_random(amount, type)
	if type == nil then type = "ex" end
	if amount == nil then amount = 1 end
	if type == "ex" then
		protlist = {"r1m1_scout01", "r1m1_scout02", "r1m1_scout03", "r1m3_MerScout", "r1m1_molokovoz01", "r1m1_molokovoz02", "r1m1_molokovoz03", 
		"r1m1_bug01", "r1m1_bug02", "r1m1_bug03", "r1m2_bug04", "r1m1_sml01", "r1m1_sml02", "r1m1_sml03", "r1m1_sml04", "r1m2_hunter02", "r1m3_hunter02", 
		"Scout01", "Scout02", "Scout03", "ArcadeScout01", "Fighter01", "Fighter02", "Fighter03", "Hunter01", "Hunter02", "Cruiser01", "Cruiser02", 
		"Dozer01", "Traktor01", "Tank01", "Bug01", "Bug02", "Molokovoz01", "Molokovoz02", "Ural00", "Ural01", "Ural02", "Belaz01", "Mirotvorec01", 
		"CoolBelaz_2", "CoolBelaz", "ArcadeBelaz", "DemoBandit", "PublicDemoBug01", "PublicDemoSinks", "PublicDemoBandit1", "PublicDemoBandit2", 
		"PublicDemoFighter", "PublicDemoIeriBand1", "PublicDemoIeriBand2", "PublicDemoIeriCar", "LisaCar", "FelixVehicle", "FelixVehicle2", 
		"AxelVehicle", "DemoFighter1", "DemoHunter1", "DemoHunter2", "DemoBug1", "DemoBug2", "DemoBug3", "DemoMolokovoz1", "DemoMolokovoz2", 
		"DemoMolokovoz3", "DemoUral1", "DemoShot1", "DemoUral2", "DemoUral3", "DemoBelaz1", "DemoBelaz2", "DemoBelaz3", "DemoMirotvorec1", 
		"DemoMirotvorec2", "DemoMirotvorec3", "Revolutioner1", "Revolutioner2", "BelazTest", "MolokovozTest", "Sml101", "Sml201", "Sml301", 
		"Sml401", "mirotvorecTest", "mirotvorecTest1", "MirotvorecForSale", "BugTest1", "BelazTest01", "BelazTest02", "BelazTest03", "BelazTest04", 
		"BelazTest05", "BelazForSale", "BugForSale", "UralForSale", "MolokovozForSale", "BelazShot", "UralShot", "MirotvorecShot", "Formula01", 
		"r1m3_Fighter01", "r1m3_Fighter02", "r1m3_Sml101", "r1m3_molokovoz03", "r1m3_molokovozInOldCity", "r2m1_Bug1", "r2m1_Fighter01", "r2m1_Fighter02", 
		"r2m1_FighterGulik", "r2m1_FighterNarcCaravan", "r2m1_Hunter01", "r2m1_Hunter02", "r2m1_HunterNarcCaravan", "r2m1_HunterNarcBoss", "r2m1_Ural01", 
		"r2m1_Belaz01", "r2m1_Molokovoz01", "r2m1_scout01", "r2m1_scout02", "r2m1_scout03", "r2m2_Molokovoz01", "r2m2_Fighter01", "r2m2_Fighter02", 
		"r2m2_Hunter01", "r2m2_scout01", "r2m2_Ural01", "RobotBobot01", "RobotBobot02", "RobotTron", "RobotMetatron", "r2m2_ShamanHunter01", 
		"r2m2_ShamanHunter02", "r1m1_CaravanBug01", "r1m1_CaravanBug02", "r1m1_CaravanBug03", "r1m1_CaravanBug04", "r1m2_CaravanBug01", "r1m2_CaravanBug02", 
		"r1m3_CaravanMolokovoz01", "r1m3_CaravanMolokovoz02", "r2m1_CaravanMolokovoz01", "r2m1_CaravanMolokovoz02", "r2m1_CaravanUral01", "r2m1_CaravanUral02", 
		"r2m2_CaravanUral01", "r2m2_CaravanUral02", "UralMenu", "BelazMenu", "MolokovozMenu", "FighterMenu", "ScoutMenu", "r1m1_CaravanGuardianSml101", 
		"r1m1_CaravanGuardianSml201", "r1m2_CaravanGuardianSml301", "r1m3_CaravanGuardianSml401", "r2m1_CaravanGuardianSml401", "r2m1_CaravanGuardianScout201", 
		"r2m2_CaravanGuardianScout301", "Gladiator02"}
	elseif type == "team" then
		if IsQuestComplete("r3m2_OracleMemory") then
			protlist = {"r1m1_scout01", "r1m1_scout02", "r1m1_scout03", "r1m3_MerScout", "r1m1_molokovoz01", "r1m1_molokovoz02", "r1m1_molokovoz03", 
						"r1m1_bug01", "r1m1_bug02", "r1m1_bug03", "r1m2_bug04", "r1m1_sml01", "r1m1_sml02", "r1m1_sml03", "r1m1_sml04", "r1m2_hunter02", "r1m3_hunter02", 
						"Scout01", "Scout02", "Scout03", "ArcadeScout01", "Fighter01", "Fighter02", "Fighter03", "Hunter01", "Hunter02", "Cruiser01", "Cruiser02", 
						"Dozer01", "Traktor01", "Tank01", "Bug01", "Bug02", "Molokovoz01", "Molokovoz02", "Ural00", "Ural01", "Ural02", "Belaz01", "Mirotvorec01", 
						"CoolBelaz_2", "CoolBelaz", "ArcadeBelaz", "DemoBandit", "PublicDemoBug01", "PublicDemoSinks", "PublicDemoBandit1", "PublicDemoBandit2", 
						"PublicDemoFighter", "PublicDemoIeriBand1", "PublicDemoIeriBand2", "PublicDemoIeriCar", "LisaCar", "FelixVehicle", "FelixVehicle2", 
						"AxelVehicle", "DemoFighter1", "DemoHunter1", "DemoHunter2", "DemoBug1", "DemoBug2", "DemoBug3", "DemoMolokovoz1", "DemoMolokovoz2", 
						"DemoMolokovoz3", "DemoUral1", "DemoShot1", "DemoUral2", "DemoUral3", "DemoBelaz1", "DemoBelaz2", "DemoBelaz3", "DemoMirotvorec1", 
						"DemoMirotvorec2", "DemoMirotvorec3", "Revolutioner1", "Revolutioner2", "BelazTest", "MolokovozTest", "Sml101", "Sml201", "Sml301", 
						"Sml401", "mirotvorecTest", "mirotvorecTest1", "MirotvorecForSale", "BugTest1", "BelazTest01", "BelazTest02", "BelazTest03", "BelazTest04", 
						"BelazTest05", "BelazForSale", "BugForSale", "UralForSale", "MolokovozForSale", "BelazShot", "UralShot", "MirotvorecShot", "Formula01", 
						"r1m3_Fighter01", "r1m3_Fighter02", "r1m3_Sml101", "r1m3_molokovoz03", "r1m3_molokovozInOldCity", "r2m1_Bug1", "r2m1_Fighter01", "r2m1_Fighter02", 
						"r2m1_FighterGulik", "r2m1_FighterNarcCaravan", "r2m1_Hunter01", "r2m1_Hunter02", "r2m1_HunterNarcCaravan", "r2m1_HunterNarcBoss", "r2m1_Ural01", 
						"r2m1_Belaz01", "r2m1_Molokovoz01", "r2m1_scout01", "r2m1_scout02", "r2m1_scout03", "r2m2_Molokovoz01", "r2m2_Fighter01", "r2m2_Fighter02", 
						"r2m2_Hunter01", "r2m2_scout01", "r2m2_Ural01", "RobotBobot01", "RobotBobot02", "RobotTron", "RobotMetatron", "r2m2_ShamanHunter01", 
						"r2m2_ShamanHunter02", "r1m1_CaravanBug01", "r1m1_CaravanBug02", "r1m1_CaravanBug03", "r1m1_CaravanBug04", "r1m2_CaravanBug01", "r1m2_CaravanBug02", 
						"r1m3_CaravanMolokovoz01", "r1m3_CaravanMolokovoz02", "r2m1_CaravanMolokovoz01", "r2m1_CaravanMolokovoz02", "r2m1_CaravanUral01", "r2m1_CaravanUral02", 
						"r2m2_CaravanUral01", "r2m2_CaravanUral02", "UralMenu", "BelazMenu", "MolokovozMenu", "FighterMenu", "ScoutMenu", "r1m1_CaravanGuardianSml101", 
						"r1m1_CaravanGuardianSml201", "r1m2_CaravanGuardianSml301", "r1m3_CaravanGuardianSml401", "r2m1_CaravanGuardianSml401", "r2m1_CaravanGuardianScout201", 
						"r2m2_CaravanGuardianScout301", "Gladiator02"}
		elseif IsQuestComplete("d_FindHouseOfBen_Quest") or IsQuestComplete("d_FindLisaOnSever_Quest") then
			protlist = {"r1m1_scout01", "r1m1_scout02", "r1m1_scout03", "r1m3_MerScout", "r1m1_molokovoz01", "r1m1_molokovoz02", "r1m1_molokovoz03", "r1m1_bug01", "r1m1_bug02", 
						"r1m1_bug03", "r1m2_bug04", "r1m1_sml01", "r1m1_sml02", "r1m1_sml03", "r1m1_sml04", "r1m2_hunter02", "r1m3_hunter02", "Scout01", "Scout02", "Scout03", 
						"Fighter01", "Fighter02", "Fighter03" , "Hunter01", "Hunter02", "Bug01", "Bug02", "Molokovoz02", "DemoBandit", "PublicDemoBug01", "PublicDemoSinks", 
						"PublicDemoBandit1", "PublicDemoBandit2", "PublicDemoFighter", "PublicDemoIeriBand1", "PublicDemoIeriBand2", "PublicDemoIeriCar", "LisaCar", 
						"FelixVehicle", "FelixVehicle2", "DemoFighter1", "DemoHunter1", "DemoHunter2", "DemoBug1", "DemoBug2", "DemoBug3", "DemoMolokovoz1", "DemoMolokovoz2", 
						"DemoMolokovoz3", "Revolutioner1", "Revolutioner2", "MolokovozTest", "Sml101", "Sml201", "Sml301", "Sml401", "BugTest1", "BugForSale", "MolokovozForSale", 
						"Formula01", "r1m3_Fighter01", "r1m3_Fighter02", "r1m3_Sml101", "r1m3_molokovoz03", "r1m3_molokovozInOldCity", "r2m1_Bug1", "r2m1_Fighter01", 
						"r2m1_Fighter02", "r2m1_FighterGulik", "r2m1_FighterNarcCaravan", "r2m1_Hunter01", "r2m1_Hunter02", "r2m1_HunterNarcCaravan", "r2m1_HunterNarcBoss", 
						"r2m1_Molokovoz01", "r2m1_scout01", "r2m1_scout02", "r2m1_scout03", "r2m2_Molokovoz01", "r2m2_Fighter01", "r2m2_Fighter02", "r2m2_Hunter01", "r2m2_scout01", 
						"r2m2_ShamanHunter01", "r2m2_ShamanHunter02", "r1m1_CaravanBug01", "r1m1_CaravanBug02", "r1m1_CaravanBug03", "r1m1_CaravanBug04", "r1m2_CaravanBug01", 
						"r1m2_CaravanBug02", "r1m3_CaravanMolokovoz01", "r1m3_CaravanMolokovoz02", "r2m1_CaravanMolokovoz01", "r2m1_CaravanMolokovoz02", "MolokovozMenu", 
						"FighterMenu", "ScoutMenu", "r1m1_CaravanGuardianSml101", "r1m1_CaravanGuardianSml201", "r1m2_CaravanGuardianSml301", "r1m3_CaravanGuardianSml401", 
						"r2m1_CaravanGuardianSml401", "r2m1_CaravanGuardianScout201", "r2m2_CaravanGuardianScout301", "RobotBobot01", "RobotBobot02", "Tank01", "Ural00", 
						"Ural01", "Ural02", "DemoUral1", "DemoShot1", "DemoUral2", "DemoUral3", "UralForSale", "UralShot", "r2m1_Ural01", "r2m2_Ural01", "r2m1_CaravanUral01", 
						"r2m1_CaravanUral02", "r2m2_CaravanUral01", "r2m2_CaravanUral02", "UralMenu", "RobotTron", "RobotMetatron"}
		else
			protlist = {"r1m1_scout01", "r1m1_scout02", "r1m1_scout03", "r1m3_MerScout", "r1m1_molokovoz01", "r1m1_molokovoz02", "r1m1_molokovoz03", "r1m1_bug01", "r1m1_bug02", 
						"r1m1_bug03", "r1m2_bug04", "r1m1_sml01", "r1m1_sml02", "r1m1_sml03", "r1m1_sml04", "r1m2_hunter02", "r1m3_hunter02", "Scout01", "Scout02", "Scout03", 
						"Fighter01", "Fighter02", "Fighter03" , "Hunter01", "Hunter02", "Bug01", "Bug02", "Molokovoz02", "DemoBandit", "PublicDemoBug01", "PublicDemoSinks", 
						"PublicDemoBandit1", "PublicDemoBandit2", "PublicDemoFighter", "PublicDemoIeriBand1", "PublicDemoIeriBand2", "PublicDemoIeriCar", "LisaCar", "FelixVehicle", 
						"FelixVehicle2", "DemoFighter1", "DemoHunter1", "DemoHunter2", "DemoBug1", "DemoBug2", "DemoBug3", "DemoMolokovoz1", "DemoMolokovoz2", "DemoMolokovoz3", 
						"Revolutioner1", "Revolutioner2", "MolokovozTest", "Sml101", "Sml201", "Sml301", "Sml401", "BugTest1", "BugForSale", "MolokovozForSale", "Formula01", 
						"r1m3_Fighter01", "r1m3_Fighter02", "r1m3_Sml101", "r1m3_molokovoz03", "r1m3_molokovozInOldCity", "r2m1_Bug1", "r2m1_Fighter01", "r2m1_Fighter02", 
						"r2m1_FighterGulik", "r2m1_FighterNarcCaravan", "r2m1_Hunter01", "r2m1_Hunter02", "r2m1_HunterNarcCaravan", "r2m1_HunterNarcBoss", "r2m1_Molokovoz01", 
						"r2m1_scout01", "r2m1_scout02", "r2m1_scout03", "r2m2_Molokovoz01", "r2m2_Fighter01", "r2m2_Fighter02", "r2m2_Hunter01", "r2m2_scout01", 
						"r2m2_ShamanHunter01", "r2m2_ShamanHunter02", "r1m1_CaravanBug01", "r1m1_CaravanBug02", "r1m1_CaravanBug03", "r1m1_CaravanBug04", "r1m2_CaravanBug01", 
						"r1m2_CaravanBug02", "r1m3_CaravanMolokovoz01", "r1m3_CaravanMolokovoz02", "r2m1_CaravanMolokovoz01", "r2m1_CaravanMolokovoz02", "MolokovozMenu", 
						"FighterMenu", "ScoutMenu", "r1m1_CaravanGuardianSml101", "r1m1_CaravanGuardianSml201", "r1m2_CaravanGuardianSml301", "r1m3_CaravanGuardianSml401", 
						"r2m1_CaravanGuardianSml401", "r2m1_CaravanGuardianScout201", "r2m2_CaravanGuardianScout301", "RobotBobot01", "RobotBobot02"}
		end
	end
	local len = getn(protlist)
	if type == "team" then
		local ListOfVehicles = {"car1"}
		for i = 1, amount do
			ListOfVehicles[i] = protlist[random(len)]
		end
		return ListOfVehicles
	elseif type == "ex" then
		ListOfVehicles = protlist[random(len)]
		return ListOfVehicles
	end
end


-- Moves player's vehicle to position
function MovePlayer( x, y, z )
	GetPlayerVehicle():SetPosition( CVector( x, y, z ) )
end


-- Moves player's vehicle to camera position
function MovePlayerToCamera()
	local pos, rot, lookAt = GetCameraPos()
	GetPlayerVehicle():SetPosition( pos )
end


function sss()
	local p = CreateDummy{ modelName ="StoneBridge",objName = "Bridge", pos = CVector( 2000, 2000, 255 ) }
end

function move( x, z )
	GetEntityByName("Team17"):SetDestination( CVector( x, 100, z ) )
end	

function die( x )
	GetEntityByName(x):AddModifier( "hp", "- 1000000" )
end	

function caravan()
	GetEntityByName("TheTown"):SpawnCaravanToLocation("TheEnd")
--	GetEntityByName("TheTown"):SpawnCaravanToLocation("TheTown_defend")
end


function save()
	g_ObjCont:SaveToFileFull( "aaa.xml" )
end

function load()
	g_ObjCont:LoadFromFileFull( "aaa.xml" )	
end

function addgold( amount )
	g_Player:AddMoney( amount )
end

function getgold()
	return g_Player:GetMoney()
end

function ff()
	Fly("testq", 0, 0, 30, 1, 1 )
end

function ffc()
	Fly("circle", 0, 0, 10, 1, 1 )
end

function ffb()
	Fly("big", 0, 0, 35, 1, 1 )
end

function ffr()
	Fly("real", 0, 0, 15, 1, 1 )
end

function fff()
	Fly("test", 0, 0, 4, 1, 1 )
	AddCinematicMessage( 8000, 3 )
	AddCinematicMessage( 1, 0.1 )
end


function testpath()
	GetEntityByName("enemy"):SetPathByName("testVehicle")
	GetEntityByName("enemy"):PlaceToEndOfPath()
end

function AddPlayerVehicle(modelname)
-- добавляет игроку машину (если только у него ее нет)
-- можно использовать, когда убъют или типа того.
-- modelname - модель машины, которую надо. По умолчанию дается Урал
    if not modelname then
		modelname="Ural01"
	end
	if GetPlayerVehicle() then
		local teamID = CreateNewObject{
				prototypeName = "team",
				objName = "TempTeam",
				belong = "1100"
			}
	  	local team=GetEntityByID(teamID)
		if team then team:AddChild(GetPlayerVehicle()) end
		team:Remove()
	end
	local id = CreateNewObject{
		prototypeName = modelname,
--	 by Anton: name is set automatically in code --	objName = "PlayerVehicle"..tostring(random(9999)),
		objName = "",
		belong = 1100
	}
	local vehicle = GetEntityByID(id)
	local pl=g_Player
	if vehicle and pl then
	    println("Car name: "..vehicle:GetName())
		local hover = 1.5 * vehicle:GetSize().y
    	local pos, yaw, pitch, roll, lookAt = GetCameraPos()
		println(pos)
		vehicle:SetPosition(pos)
		pl:AddChild(vehicle)
    end
end

function AddPlayerNewVehicle(modelname)
-- добавляет игроку машину вместо текущей
-- modelname - модель машины, которую надо. По умолчанию дается Урал

    if not modelname then
		modelname="Ural01"
	end

	local realpos
	local Plf = GetPlayerVehicle()

	if Plf then
		realpos = Plf:GetPosition()
		local teamID = CreateNewObject{
				prototypeName = "team",
				objName = "TempTeam",
				belong = "1100"
			}
	  	local team=GetEntityByID(teamID)
		if team then team:AddChild(GetPlayerVehicle()) end
		team:Remove()
	end

	local id = CreateNewObject{
		prototypeName = modelname,
--	 by Anton: name is set automatically in code --			objName = "PlayerVehicle"..tostring(random(9999)),
		objName = "",
		belong = 1100
	}

	local vehicle = GetEntityByID(id)

	local pl = g_Player

	if vehicle and pl then
		local hover = 1.5 * vehicle:GetSize().y
		vehicle:SetPosition(realpos)
		pl:AddChild(vehicle)
    end
end

function fa()
	FlyAround( 2, -0.5, 30, 5, CVector(60, 300, 60), GetPlayerVehicleId(), 1, 1 )
end

function fl()
	GetPlayerVehicle():SetCustomControlEnabled(1)
	GetPlayerVehicle():SetThrottle(1.0)
	FlyLinked("relative", GetPlayerVehicleId(), 10, 1, 1)
end

function fl2()
	GetPlayerVehicle():SetCustomControlEnabled(1)
	GetPlayerVehicle():SetThrottle(1.0)
	FlyLinked("relative", GetPlayerVehicleId(), 10, 1, 1)
end


function dsc()
	GetPlayerVehicle():SetCustomControlEnabled(0)
end

function tec()
	CreateEffect("ET_PS_BIGWHEELGRASSSPLASH", CVector(60, 250, 60), Quaternion(0, 0, 0, 1), 100, 0 )
	CreateEffect("ET_PS_BIGWHEELGRASSSPLASH", CVector(70, 250, 70), Quaternion(0, 0, 0, 1), 0, 1 )
end 

function tgr()
	local Workshop = GetEntityByName("TheTown_Workshop")
	local Repository = Workshop:GetRepositoryByTypename("CabinsAndBaskets")
	Repository:AddItems("belazCab01", 2)
end

function trailer( enable )
	if enable ~= 0 then
		GetPlayerVehicle():AttachTrailer("MolokovozTrailer")
	else
		GetPlayerVehicle():DetachTrailer()
	end
end


function CreateDummy( prototype, modelName, mass, pos )
	println(prototype)

	local objId = CreateNewObject{ prototypeName = prototype, objName="ddd" }
	local obj = GetEntityByID( objId )

	obj:SetModelName( modelName )
	obj:SetMass( mass )
	obj:SetPosition( pos )
end

function PlayerDie()
	GetPlayerVehicle():AddModifier("hp", "- 1000000" )
end

function  bbb()
	getObj("boss"):StartMoving(CVector(200,300,200),CVector(1,0,0))
end

function  bbb1()
	getObj("boss"):StartMoving(CVector(100,270,100),CVector(0,0,1))
end

function relCoord(name)
	local veh=GetPlayerVehicle()
	if name then 
		local vehtmp = GetEntityByName(name)
		if vehtmp then
		   veh = vehtmp
		else
			println("Object with name "..name.." not exists")
		end
	end

	local campos, camrot = GetCameraPos()
	local vehpos = veh:GetPosition()
	local pos=campos-vehpos
	local rot=camrot
    LOG(' <Point  ')
    LOG('    coord="' .. strsub( tostring(pos), 2, strlen( tostring(pos) ) - 1 ) .. '"')
    LOG('    rotation="'.. strsub( tostring(rot), 2, strlen( tostring(rot) ) - 1 ) .. '"/>')
end


function CreateEnemy(modelname)
-- создает врага в позиции камеры
    if not modelname then
		modelname="Ural01"
	end

	local enemyname = "EnemyTeam"..tostring(random(9999))

	local teamID = CreateNewObject{
			prototypeName = "team",
			objName = enemyname,
			belong = "1002"
		}
  	local team=GetEntityByID(teamID)

	local id = CreateNewObject{
		prototypeName = modelname,
		objName = "PlayerVehicle"..tostring(random(9999)),
		belong = "1002"
	}
	local vehicle = GetEntityByID(id)

	if vehicle and team then
		local hover = 1.5 * vehicle:GetSize().y
    	local pos = GetCameraPos()
		vehicle:SetPosition(pos)
		vehicle:SetRandomSkin()
		team:AddChild(vehicle)
    end

    println(enemyname)
end

function SetGameTime( h, m )

	if g_ObjCont ~= nil then
		local CurrentDate = g_ObjCont:GetGameTime().AsNumList

		g_ObjCont:SetGameTime( h, m, CurrentDate[2], CurrentDate[3], CurrentDate[4] )
		UpdateWeather()
	end

end