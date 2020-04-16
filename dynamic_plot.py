import pylab
import numpy as np

class DynamicPlot(object):
    def __init__(self, groups=1, items=1, hatch=False):
        self.groups = groups
        self.items = items
        self.hatch = hatch
        self.font_size = 22
        self.legend_font = 15
        
        self.colors = ['royalblue', 'cyan', \
                            'orange', 'yellow', 'green']
        self.hatches = ['//', '+', 'x', '\\', 'o']

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups):
        if groups < 1:
            raise ValueError("Groups can not be less than 1")
        self._groups = groups

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        if items < 1:
            raise ValueError("Items can not be less than 1")
        self._items = items
        
    @property
    def hatch(self):
        return self._hatch

    @hatch.setter
    def hatch(self, hatch):
        self._hatch = hatch
        
    @property
    def font_size(self):
        return self._font_size
    
    @font_size.setter
    def font_size(self, font_size):
        if font_size < 6:
            raise ValueError("Font size should be greater equal 6")
        self._font_size = str(font_size)
#        self._legend_size = font_size - 3

    def plot(self, data, error=None, item_labels=None, \
            group_labels=None, filename=None, title=None):
        assert data.shape==(self.groups, self.items), \
                "Data matrix should be of size (groups, items)"
        if error is not None:
            assert error.shape==(self.groups, self.items), \
                    "Error matrix should be of size (groups, items)"
        if item_labels is not None:
            assert len(item_labels)==self.items, \
                    "Labels should be of length=items"
        if group_labels is not None:
            assert len(group_labels)==self.groups, \
                    "Labels should be of length=groups"

        bar_width = 0.5 if self._items==1 else (0.5-0.1*(self._items - 1))

        pylab.figure()
        
        r0 = np.arange(self.groups)
        r = [[x + i*bar_width for x in r0] for i in range(1,self.groups)]
        r = [list(r0)] + r
        
        for i in range(self.items):
            
            error_vec = error[:,i] if error is not None else None
            label = item_labels[i] if item_labels is not None else None
            
            if self.hatch:
                pylab.bar(r[i], data[:,i], width=bar_width, color='black', \
                    edgecolor='white', yerr=error_vec, hatch=self.hatches[i], \
                    capsize=6, label=label)
            else:
                pylab.bar(r[i], data[:,i], width=bar_width, color=self.colors[i], \
                        edgecolor='black', yerr=error_vec, capsize=6, label=label)

        pylab.xticks([r + (0.5*(self.items-1))*bar_width \
                      for r in range(self.groups)], group_labels,
                        fontweight='bold',fontsize=self.font_size)
        pylab.yticks(fontweight='bold',fontsize=self.font_size)
        
        if item_labels is not None:
            pylab.legend(loc=1, prop={'size':self.legend_font, 
                                      'weight':'bold'})
        
        if title is not None:
            pylab.title(title, fontweight='bold', fontsize=self.font_size)
        
        if filename is not None:
            pylab.savefig(filename)


if __name__=="__main__":
    z = DynamicPlot(groups=3, items=3, hatch=False)
    data = 5 + 2*np.random.rand(3,3)
    err = np.random.rand(3,3)
    
    z.plot(data, error=err, item_labels=['1','2','3'], 
           group_labels=['g1','g2','g3'], title='Test')
        
