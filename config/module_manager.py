import logging

logger = logging.getLogger(__name__)

class ModuleManager:
    """Manage additional modules"""
    
    def __init__(self):
        self.modules = {}
        self.active_modules = []
    
    def register_module(self, module_name, module_class):
        """Register new module"""
        self.modules[module_name] = module_class
        logger.info(f"Module registered: {module_name}")
    
    def load_module(self, module_name):
        """Load module"""
        if module_name in self.modules:
            try:
                module_instance = self.modules[module_name]()
                self.active_modules.append((module_name, module_instance))
                logger.info(f"Module loaded: {module_name}")
                return module_instance
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")
        return None
    
    def unload_module(self, module_name):
        """Unload module"""
        self.active_modules = [(name, mod) for name, mod in self.active_modules 
                               if name != module_name]
        logger.info(f"Module unloaded: {module_name}")
    
    def get_active_modules(self):
        """Get active modules"""
        return self.active_modules
