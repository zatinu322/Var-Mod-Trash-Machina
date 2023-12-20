LOG("Activating randomizer scripts...")

local function _CreateNewObject( prototypeName, objName, parentId, belong )
	local prototypeId = g_ObjCont:GetPrototypeId( prototypeName )

	return g_ObjCont:CreateNewObject( prototypeId, objName, parentId, belong )
end

function giveguns_random (Name)
    if Name == nil then
        veh=GetPlayerVehicle()
    else
        veh=getObj(Name)
    end
    local parts={"CABIN_","BASKET_","CHASSIS_"}
    local slots={"SMALL_","BIG_","GIANT_","SIDE_"}
    local guns={"GUN","GUN_0","GUN_1","GUN_2"}
    local smallgun = RAND_GUNS_1
    local sidegun = RAND_GUNS_2
    local i,j,k=1,1,1
    while parts[i] do
        while slots[j] do
            while guns[k] do
                local gun=1
                local slot=parts[i]..slots[j]..guns[k]
                if j == 4 then
                    gun = sidegun[random(getn(sidegun))]
                else
                    gun = smallgun[random(getn(smallgun))]
                end
                
                if veh:CanPartBeAttached(slot) then
                    veh:SetNewPart(slot,gun)
                end
                k=k+1
            end
            k=1
            j=j+1
        end
        j=1
        i=i+1
    end

    veh = nil
end

function CreateNewDummyObject(modelName, objName, parentId, belong, pos, rot,skin)
	local prototypeName 	=  	"someDummyObject"
	local dObj		=	_CreateNewObject( prototypeName, objName, parentId, belong )
	local obj		=	GetEntityByID (dObj)

	if skin == nil then skin = 0 end

	if RAND_DWELLER then
		local dweller_list = RAND_DWELLER_1
		local len = getn(dweller_list)

		for i = 1,len do
			if modelName == dweller_list[i] then
				modelName = dweller_list[random(len)]
			end
		end
	end

	obj:SetModelName(modelName)
	obj:SetRotation ( rot )
	obj:SetPosition ( pos )
	obj:SetSkin ( skin )
end

function CreateTeam(Name, Belong, CreatePos, ListOfVehicle, WalkPos, IsWares, Rotate)
    local teamID = CreateNewObject{
            prototypeName = "team",
            objName = Name,
            belong = Belong
        }
    local team=GetEntityByID(teamID)
    if team then
        local i=1
        local id=0

        if RAND_VEH then
            local len = getn(ListOfVehicle)
            ListOfVehicle = prot_random(len, "team")
        end

        while ListOfVehicle[i] do
            local id = CreateNewObject{
                        prototypeName = ListOfVehicle[i],
                        objName = Name.."_vehicle_"..i-1,
                        belong = Belong
                    }
            local vehicle = GetEntityByID(id)
            if vehicle then
                vehicle:SetRandomSkin()
                if IsWares==1 then
                    local mapNum = 0
                    local mapName = GET_GLOBAL_OBJECT( "CurrentLevel" ):GetLevelName()
                    if mapName == "r1m1" then mapNum = 0 end
                    if mapName == "r1m2" then mapNum = 1 end
                    if mapName == "r1m3" then mapNum = 1 end
                    if mapName == "r1m4" then mapNum = 2 end
                    if mapName == "r2m1" then mapNum = 3 end
                    if mapName == "r2m2" then mapNum = 4 end
                    if mapName == "r3m1" then mapNum = 5 end
                    if mapName == "r3m2" then mapNum = 6 end
                    if mapName == "r4m1" then mapNum = 7 end
                    if mapName == "r4m2" then mapNum = 8 end

                    local RandWarez = {"potato","firewood","scrap_metal","oil","fuel","machinery","bottle","tobacco","book","electronics"}
                    local r = random(2) + mapNum

                    vehicle:AddItemsToRepository(RandWarez[r], 1)
                end
            
                if Rotate then
                    vehicle:SetRotation(Quaternion(Rotate))
                end
                vehicle:SetGamePositionOnGround(CreatePos)
            
                team:AddChild(vehicle)
                local vh_length=1.7 * vehicle:GetSize().z
                CreatePos.z=CreatePos.z+vh_length
                
                if RAND_GUNS then
                    giveguns_random(vehicle)
                end
            end
            i = i + 1
        end
    else
       println("Error: Can't create team !!!")
       return 0
    end
        if WalkPos then
            team:SetDestination(WalkPos)
        end
    return team
end

function CreateVehicleEx( PrototypeName, Name, pos, belong )
	local bel

	if belong then
		bel = belong
	else
		bel = 1100
	end

	if RAND_VEH then
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

	vehicle:SetGamePositionOnGround( pos )

	if RAND_GUNS then
		giveguns_random(Name)
	end

	return vehicle
end

function prot_random(amount, type)
	if type == nil then type = "ex" end
	if amount == nil then amount = 1 end

	if type == "ex" then
		protlist = RAND_VEH_3
	elseif type == "team" then
		if IsQuestComplete("r3m2_OracleMemory") then
			protlist = RAND_VEH_3
		elseif IsQuestComplete("d_FindHouseOfBen_Quest") or IsQuestComplete("d_FindLisaOnSever_Quest") then
			protlist = RAND_VEH_2
		else
			protlist = RAND_VEH_1
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

LOG("Randomizer scripts activated.")