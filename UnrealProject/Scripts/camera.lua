-- Copyright 2016, 2017 Mario Ynocente Castro, Mathieu Bernard
--
-- You can redistribute this file and/or modify it under the terms of
-- the GNU General Public License as published by the Free Software
-- Foundation, either version 3 of the License, or (at your option) any
-- later version.
--
-- This program is distributed in the hope that it will be useful, but
-- WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
-- General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program. If not, see <http://www.gnu.org/licenses/>.


-- This module manages the scene's camera. It defines and controls
-- it's location and rotation. The other camera parameters are
-- constant and fixed in the Uneral editor: a perspective projection,
-- a fixed ratio heigth/width at 1 and an horizontal field of view of
-- 90 degrees.


local uetorch = require 'uetorch'
local utils = require 'utils'


local M = {}


-- The camera actor defined in the scene, initialized during the first
-- call to the get_actor() function
local camera_actor


-- Return the camera actor defined in the scene
function M.get_actor()
   if not camera_actor then
      -- Unreal renames the camera accidentally when the MainMap
      -- blueprint is modified, so we also try other known names for
      -- that actor...
      local known_names = {
         'Camera',
         'MainMap_CameraActor_Blueprint_C_0',
         'MainMap_CameraActor_Blueprint_C_1'}

      -- search the real name in the known names
      for _, n in ipairs(known_names) do
         local a = uetorch.GetActor(n)
         if a then
            camera_actor = a
            break
         end
      end

      -- make sure we found the camera
      assert(camera_actor)
   end

   return camera_actor
end


-- Return a random location vector for the camera
function M.random_location()
   return {
      x = 150 + math.random(-100, 100),
      y = 30 + math.random(200, 400),
      z = 80 + math.random(-10, 100)
   }
end


-- Return a random rotation vector for the camera
function M.random_rotation()
   return {
      pitch = math.random(-15, 10),
      yaw = -90 + math.random(-30, 30),
      roll = 0
   }
end


-- Return random parameters for the camera
function M.get_random_parameters()
   return {
      location = M.random_location(),
      rotation = M.random_rotation()
   }
end


-- Return default parameters for the camera
function M.get_default_parameters()
   return {
      location = {x = 150, y = 30, z = 80},
      rotation = {pitch = 0, yaw = -90, roll = 0}
   }
end


-- Setup the camera location and rotation
--
-- If params are not specified, use default parameters. `params` must
-- be a table structured as {location = {x, y, z}, rotation = {pitch,
-- yaw, roll}}
function M.setup(params)
   if not params then
      params = M.get_default_parameters()
   end

   uetorch.SetActorLocation(
      M.get_actor(),
      params.location.x,
      params.location.y,
      params.location.z)

   uetorch.SetActorRotation(
      M.get_actor(),
      params.rotation.pitch,
      params.rotation.yaw,
      params.rotation.roll)
end


-- Return the camera location and rotation as a string
function M.get_status()
   return utils.coordinates_to_string(M.get_actor())
end


return M
