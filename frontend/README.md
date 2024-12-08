# Mycodo Frontend Migration Project

This project aims to modernize the Mycodo frontend using React, TypeScript, and modern web technologies. The new frontend will provide a more responsive, maintainable, and feature-rich user interface while maintaining all existing functionality.

## Technology Stack

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI
- **State Management**: React Query
- **Routing**: React Router
- **API Client**: Axios
- **Development Tools**: ESLint, TypeScript ESLint

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── dashboard/
│   │   ├── devices/
│   │   ├── camera/
│   │   ├── methods/
│   │   └── settings/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   └── utils/
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Development Roadmap

### Phase 1: Core Infrastructure (Week 1)

#### 1. Authentication System
- Login/logout functionality
- Password reset flow
- Admin user creation
- JWT token management
- Protected routes
- Authentication context

#### 2. API Integration Layer
- API client setup with Axios
- Type definitions for API responses
- Error handling middleware
- Request/response interceptors
- API route constants

### Phase 2: Dashboard & Monitoring (Week 2)

#### 1. Dashboard Framework
- Customizable dashboard grid
- Widget system
- Real-time data updates
- Dashboard settings
- Layout persistence

#### 2. Monitoring Components
- Live readings display
- Graph components (D3.js)
- Real-time data visualization
- Time-series data handling
- Export functionality

### Phase 3: Device Management (Week 2-3)

#### 1. Input Management
- Input device configuration
- Sensor readings display
- Input options management
- Calibration interface
- Input testing tools

#### 2. Output Control
- Output device management
- Manual control interface
- Output scheduling
- PWM control
- Output testing

### Phase 4: Camera & Media (Week 3)

#### 1. Camera Management
- Camera stream display
- Camera settings
- Image capture
- Video recording
- Timelapse functionality

#### 2. Media Browser
- Image/video gallery
- Media organization
- Download functionality
- Stream viewer

### Phase 5: Advanced Features (Week 4)

#### 1. Methods & Functions
- PID controller interface
- Method creation/editing
- Function management
- Conditional functions
- Trigger system

#### 2. Data Analysis
- Data logging interface
- Export functionality
- Graph customization
- Statistical analysis
- Data visualization

### Phase 6: System & Settings (Week 4-5)

#### 1. System Management
- System information display
- Resource monitoring
- Update management
- Backup/restore
- Log viewer

#### 2. Settings & Configuration
- General settings
- User management
- Email notifications
- Unit configuration
- System preferences

## Component Examples

### API Integration

```typescript
// src/services/api.ts
export const deviceApi = {
  getDevices: () => axios.get<Device[]>('/api/devices'),
  updateDevice: (id: string, data: Partial<Device>) => 
    axios.put(`/api/devices/${id}`, data),
};
```

### Custom Hooks

```typescript
// src/hooks/useDevice.ts
export function useDevice(deviceId: string) {
  return useQuery(['device', deviceId], () => 
    deviceApi.getDevice(deviceId));
}

// src/hooks/useMeasurements.ts
export function useMeasurements(deviceId: string) {
  return useQuery(['measurements', deviceId], () => 
    deviceApi.getMeasurements(deviceId), {
    refetchInterval: 5000, // Real-time updates
  });
}
```

### Type Definitions

```typescript
// src/types/api.ts
interface Device {
  id: string;
  name: string;
  type: 'input' | 'output';
  measurements?: Measurement[];
}

interface Measurement {
  id: string;
  value: number;
  unit: string;
  timestamp: string;
}
```

## Getting Started

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Development Guidelines

1. **Type Safety**
   - Use TypeScript strict mode
   - Define interfaces for all API responses
   - Avoid using `any` type

2. **Component Structure**
   - Use functional components
   - Implement proper prop typing
   - Follow React hooks best practices

3. **State Management**
   - Use React Query for server state
   - Implement proper caching strategies
   - Handle loading and error states

4. **Code Style**
   - Follow ESLint configuration
   - Use consistent naming conventions
   - Write meaningful comments

5. **Testing**
   - Write unit tests for components
   - Test API integration
   - Implement E2E tests for critical flows

## Contributing

1. Create a feature branch
2. Implement changes
3. Write/update tests
4. Submit pull request

## Notes

- Maintain backward compatibility with existing API
- Focus on responsive design
- Implement proper error handling
- Consider offline functionality
- Optimize for performance

This roadmap serves as a living document and will be updated as the project progresses.
