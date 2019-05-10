import vtk
import os
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

class ofsurf:
    def __init__(self, case_dir, filename, time = None):
        self.filename = filename
        if time == None:
            self.time = self._getLatestTime(case_dir + "/postProcessing/surfaces/")
        else:
            self.time = str(time)
        
        file = case_dir + "/postProcessing/surfaces/" + self.time + "/" + filename
        
        reader = vtk.vtkDataSetReader()
        reader.SetFileName(file)
        reader.ReadAllScalarsOn()
        reader.ReadAllVectorsOn()
        reader.Update()

        data = reader.GetOutput()
        triangles = data.GetPolys().GetData()
        points = data.GetPoints()

        self.mapper = vtk.vtkCellDataToPointData()
        self.mapper.AddInputData(data)
        self.mapper.Update()

        self.ntri = triangles.GetNumberOfTuples()//4
        self.npts = points.GetNumberOfPoints()
                
        self.tri = np.zeros((self.ntri, 3))
        self.x = np.zeros(self.npts)
        self.y = np.zeros(self.npts)

        for i in range(0, self.ntri):
            self.tri[i, 0] = triangles.GetTuple(4*i + 1)[0]
            self.tri[i, 1] = triangles.GetTuple(4*i + 2)[0]
            self.tri[i, 2] = triangles.GetTuple(4*i + 3)[0]

        for i in range(0, self.npts):
            pt = points.GetPoint(i)
            self.x[i] = pt[0]
            self.y[i] = pt[1]

    def getVelocity(self):
        vels = mapper.GetOutput().GetPointData().GetArray('U')
        nvls = vels.GetNumberOfTuples()
        ux = np.zeros(nvls)
        uy = np.zeros(nvls)
        u = np.zeros(nvls)

        for i in range(0, nvls):
            U = vels.GetTuple(i)
            ux[i] = U[0]
            uy[i] = U[1]
            u[i] = np.sqrt(ux[i] ** 2 + uy[i] ** 2)
        return u
    
    def getScalarField(self, fieldname = None):
        if fieldname == None:
            fieldname = self.filename.split('_')[0]
        field = vtk_to_numpy(self.mapper.GetOutput().GetPointData().GetArray(fieldname))
        return field
    
    def _getLatestTime(self,path):
        dirs = sorted(os.listdir(path))
        return dirs[-1]