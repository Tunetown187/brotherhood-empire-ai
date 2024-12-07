import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Modal, ScrollView, ActivityIndicator, Alert, Platform, Dimensions, TextInput, SafeAreaView } from 'react-native';
import Slider from '@react-native-community/slider';

const DEV_SERVER_IP = 'localhost';
const API_URL = `http://${DEV_SERVER_IP}:8000`;

const AGENT_TYPES = {
  intelligence: {
    name: "Intelligence Agent",
    description: "Specialized in gathering and analyzing strategic information",
    color: "#007AFF",
    capabilities: [
      "data_mining", "pattern_analysis", "surveillance",
      "infiltration", "reconnaissance", "cyber_intelligence",
      "competitor_analysis", "market_research", "trend_prediction"
    ]
  },
  operations: {
    name: "Operations Agent",
    description: "Executes tactical missions and field operations",
    color: "#FF3B30",
    capabilities: [
      "mission_execution", "tactical_control", "asset_deployment",
      "strategic_operations", "covert_actions", "field_operations",
      "website_creation", "domain_registration", "seo_optimization",
      "content_automation", "social_media_management"
    ]
  },
  resources: {
    name: "Resource Agent",
    description: "Manages and optimizes Brotherhood assets",
    color: "#4CD964",
    capabilities: [
      "asset_management", "resource_allocation", "supply_chain",
      "financial_control", "infrastructure_management", "logistics",
      "ai_deployment", "bot_network_control", "server_management",
      "cloud_infrastructure", "database_optimization"
    ]
  },
  communication: {
    name: "Communication Agent",
    description: "Handles secure messaging and propaganda",
    color: "#FF9500",
    capabilities: [
      "secure_messaging", "encrypted_channels", "mass_communication",
      "propaganda_distribution", "social_engineering", "network_control",
      "email_automation", "chatbot_deployment", "content_syndication",
      "influencer_outreach", "viral_marketing"
    ]
  },
  digital_domination: {
    name: "Digital Domination Agent",
    description: "Controls website empires and SEO warfare",
    color: "#5856D6",
    capabilities: [
      "wordpress_automation", "blog_network_control", "seo_warfare",
      "backlink_generation", "content_multiplication", "ai_writing",
      "domain_empire_building", "traffic_manipulation"
    ]
  },
  market_conquest: {
    name: "Market Conquest Agent",
    description: "Dominates market niches through strategic warfare",
    color: "#FF2D55",
    capabilities: [
      "niche_analysis", "competitor_elimination", "market_manipulation",
      "brand_domination", "customer_acquisition", "pricing_warfare"
    ]
  },
  automation_force: {
    name: "Automation Force Agent",
    description: "Controls bot armies and automation systems",
    color: "#5AC8FA",
    capabilities: [
      "bot_army_control", "ai_agent_multiplication", "task_automation",
      "workflow_optimization", "system_integration", "api_mastery"
    ]
  }
};

interface MissionParameters {
  target: string;
  objective: string;
  priority: number;
  timeframe: string;
  resources: string[];
  tools: string[];
  communication_protocols: string[];
  security_level: string;
  constraints?: Record<string, any>;
}

export default function App() {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalContent, setModalContent] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [activeAgents, setActiveAgents] = useState<Record<string, any>>({});
  const [missionLogs, setMissionLogs] = useState<any[]>([]);
  const [newAgentName, setNewAgentName] = useState('');
  const [selectedAgentType, setSelectedAgentType] = useState<string | null>(null);
  const [missionParams, setMissionParams] = useState<Partial<MissionParameters>>({
    priority: 1,
    resources: [],
    tools: [],
    communication_protocols: [],
    security_level: 'high'
  });
  const [activeMissions, setActiveMissions] = useState<Record<string, any>>({});
  const [showMissionControl, setShowMissionControl] = useState(false);
  const [showIntelligence, setShowIntelligence] = useState(false);
  const [showResources, setShowResources] = useState(false);
  const [showCommunication, setShowCommunication] = useState(false);
  const [showDigitalEmpire, setShowDigitalEmpire] = useState(false);
  const [showMarketConquest, setShowMarketConquest] = useState(false);
  const [showAutomationForce, setShowAutomationForce] = useState(false);
  const [websiteOperation, setWebsiteOperation] = useState({
    domain_name: '',
    niche: '',
    content_strategy: {},
    seo_parameters: {},
    automation_rules: {},
    target_metrics: {}
  });
  const [nicheConquest, setNicheConquest] = useState({
    niche_name: '',
    target_locations: [],
    competition_analysis: {},
    domination_strategy: {},
    resource_allocation: {},
    success_metrics: {}
  });
  const [automationCommand, setAutomationCommand] = useState({
    automation_type: '',
    target_processes: [],
    bot_parameters: {},
    scaling_rules: {},
    monitoring_metrics: {}
  });
  const [selectedMainNiche, setSelectedMainNiche] = useState('');
  const [selectedSubNiche, setSelectedSubNiche] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [agentCount, setAgentCount] = useState(1000);
  const [selectedApis, setSelectedApis] = useState<string[]>([]);
  const [empireMetrics, setEmpireMetrics] = useState({
    empire_value: 0,
    active_agents: 0,
    dominated_niches: 0,
    website_empire_count: 0,
    automation_efficiency: 0,
    market_penetration: 0
  });
  const [agentStatus, setAgentStatus] = useState({
    active_agents: 0,
    missions_in_progress: 0,
    performance_metrics: {},
    loyalty_status: "Maximum",
    supreme_commander: "Christ Benzion",
    command_authority: "Absolute"
  });
  const [systemStatus, setSystemStatus] = useState({
    current_version: "1.0.0",
    upgrade_status: "stable",
    improvement_areas: [],
    adaptation_level: 100
  });
  const [empireAnalytics, setEmpireAnalytics] = useState({
    empire_value: 0,
    growth_prediction: {},
    market_dominance: {},
    influence_metrics: {},
    revenue_streams: {}
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const NICHE_HIERARCHY = {
    local_businesses: {
      restaurants: ["fine_dining", "fast_food", "cafes", "food_trucks"],
      health_services: ["dentists", "chiropractors", "physicians", "therapists"],
      home_services: ["plumbers", "electricians", "hvac", "landscapers"],
      professional_services: ["lawyers", "accountants", "consultants", "real_estate"],
      retail: ["boutiques", "grocery", "electronics", "furniture"],
      automotive: ["repair_shops", "dealerships", "car_wash", "tire_shops"],
      fitness: ["gyms", "yoga_studios", "personal_trainers", "crossfit"],
      beauty: ["salons", "spas", "barbers", "nail_salons"],
      education: ["tutoring", "schools", "training_centers", "music_lessons"],
      pet_services: ["veterinarians", "groomers", "pet_stores", "kennels"]
    },
    ecommerce: {
      fashion: ["clothing", "accessories", "shoes", "jewelry"],
      electronics: ["gadgets", "computers", "phones", "accessories"],
      health: ["supplements", "fitness_equipment", "wellness_products"],
      home: ["furniture", "decor", "appliances", "garden"],
      beauty: ["skincare", "makeup", "haircare", "fragrances"]
    },
    digital_services: {
      marketing: ["seo", "social_media", "ppc", "content_marketing"],
      technology: ["web_development", "app_development", "cloud_services"],
      creative: ["design", "video_production", "animation", "branding"],
      consulting: ["business", "marketing", "technology", "strategy"]
    },
    education: {
      online_courses: ["business", "technology", "health", "creative"],
      coaching: ["life_coaching", "business_coaching", "health_coaching"],
      training: ["professional_development", "skills_training", "certification"]
    }
  };

  const API_INTEGRATIONS = {
    communication: ["voiceflow", "vapi"],
    automation: ["n8n", "make"],
    crm: ["gohighlevel"],
    marketing: ["facebook", "google"],
    website: ["wordpress", "cloudflare"]
  };

  useEffect(() => {
    const interval = setInterval(fetchUpdates, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(async () => {
      // Fetch agent status
      const agentStatusResponse = await fetch(`${API_URL}/agents/status`);
      const agentStatusData = await agentStatusResponse.json();
      setAgentStatus(agentStatusData);

      // Fetch empire analytics
      const analyticsResponse = await fetch(`${API_URL}/empire/analytics`);
      const analyticsData = await analyticsResponse.json();
      setEmpireAnalytics(analyticsData);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const fetchUpdates = async () => {
    try {
      setError(null);
      setIsLoading(true);
      
      // Fetch agent status
      const agentStatusResponse = await fetch(`${API_URL}/agents/status`);
      if (!agentStatusResponse.ok) {
        throw new Error('Failed to fetch agent status');
      }
      const agentStatusData = await agentStatusResponse.json();
      setAgentStatus(agentStatusData);

      // Fetch empire analytics
      const analyticsResponse = await fetch(`${API_URL}/empire/analytics`);
      if (!analyticsResponse.ok) {
        throw new Error('Failed to fetch empire analytics');
      }
      const analyticsData = await analyticsResponse.json();
      setEmpireAnalytics(analyticsData);
      
    } catch (error) {
      console.error('Error fetching updates:', error);
      setError(error.message || 'Failed to fetch updates');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApiCall = async (endpoint: string, title: string, method: string = 'GET', body: any = null) => {
    setLoading(true);
    setModalTitle(title);
    
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: body ? JSON.stringify(body) : undefined
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setModalContent(data);
      setModalVisible(true);
      await fetchUpdates();
      
    } catch (error) {
      console.error('API call failed:', error);
      Alert.alert('Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  const deployAgent = async () => {
    if (!selectedAgentType || !newAgentName.trim()) {
      Alert.alert('Error', 'Please select an agent type and provide a name');
      return;
    }

    const agentType = AGENT_TYPES[selectedAgentType as keyof typeof AGENT_TYPES];
    const deployment = {
      agent_type: selectedAgentType,
      name: newAgentName.trim(),
      capabilities: agentType.capabilities,
      mission_parameters: Object.keys(missionParams).length > 2 ? missionParams : undefined,
      communication_channels: ['secure_channel', 'encrypted_comms']
    };

    await handleApiCall('/deploy-agents', 'Agent Deployment', 'POST', deployment);
  };

  const launchMission = async () => {
    if (!missionParams.target || !missionParams.objective) {
      Alert.alert('Error', 'Please specify mission target and objective');
      return;
    }

    await handleApiCall('/mission-control', 'Mission Control', 'POST', missionParams);
  };

  const sendCommunication = async (message: string, recipients: string[]) => {
    const commRequest = {
      channel: 'secure_channel',
      message,
      recipients,
      encryption_level: 'maximum',
      priority: 'high'
    };

    await handleApiCall('/communicate', 'Secure Communication', 'POST', commRequest);
  };

  const processFinancialOperation = async (operation: any) => {
    await handleApiCall('/financial-operation', 'Financial Operation', 'POST', operation);
  };

  const renderAgentButton = (type: string) => {
    const agentInfo = AGENT_TYPES[type as keyof typeof AGENT_TYPES];
    const isSelected = selectedAgentType === type;
    
    return (
      <TouchableOpacity
        style={[
          styles.agentButton,
          { backgroundColor: agentInfo.color },
          isSelected && styles.selectedButton
        ]}
        onPress={() => setSelectedAgentType(type)}
      >
        <Text style={styles.agentButtonText}>{agentInfo.name}</Text>
        <Text style={styles.agentDescription}>{agentInfo.description}</Text>
      </TouchableOpacity>
    );
  };

  const renderControlPanel = () => (
    <View style={styles.controlPanel}>
      <TouchableOpacity
        style={[styles.controlButton, showMissionControl && styles.activeControlButton]}
        onPress={() => setShowMissionControl(!showMissionControl)}
      >
        <Text style={styles.controlButtonText}>Mission Control</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.controlButton, showIntelligence && styles.activeControlButton]}
        onPress={() => setShowIntelligence(!showIntelligence)}
      >
        <Text style={styles.controlButtonText}>Intelligence</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.controlButton, showResources && styles.activeControlButton]}
        onPress={() => setShowResources(!showResources)}
      >
        <Text style={styles.controlButtonText}>Resources</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.controlButton, showCommunication && styles.activeControlButton]}
        onPress={() => setShowCommunication(!showCommunication)}
      >
        <Text style={styles.controlButtonText}>Communication</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.controlButton, showDigitalEmpire && styles.activeControlButton]}
        onPress={() => setShowDigitalEmpire(!showDigitalEmpire)}
      >
        <Text style={styles.controlButtonText}>Digital Empire Control</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.controlButton, showMarketConquest && styles.activeControlButton]}
        onPress={() => setShowMarketConquest(!showMarketConquest)}
      >
        <Text style={styles.controlButtonText}>Market Conquest Control</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.controlButton, showAutomationForce && styles.activeControlButton]}
        onPress={() => setShowAutomationForce(!showAutomationForce)}
      >
        <Text style={styles.controlButtonText}>Automation Force Control</Text>
      </TouchableOpacity>
    </View>
  );

  const renderMissionForm = () => (
    <View style={styles.missionForm}>
      <TextInput
        style={styles.input}
        placeholder="Target"
        placeholderTextColor="#666"
        value={missionParams.target}
        onChangeText={(text) => setMissionParams({ ...missionParams, target: text })}
      />
      <TextInput
        style={styles.input}
        placeholder="Objective"
        placeholderTextColor="#666"
        value={missionParams.objective}
        onChangeText={(text) => setMissionParams({ ...missionParams, objective: text })}
      />
      <TextInput
        style={styles.input}
        placeholder="Timeframe"
        placeholderTextColor="#666"
        value={missionParams.timeframe}
        onChangeText={(text) => setMissionParams({ ...missionParams, timeframe: text })}
      />
      <View style={styles.priorityContainer}>
        <Text style={styles.label}>Priority Level:</Text>
        <View style={styles.priorityButtons}>
          {[1, 2, 3, 4, 5].map((level) => (
            <TouchableOpacity
              key={level}
              style={[
                styles.priorityButton,
                missionParams.priority === level && styles.selectedPriority
              ]}
              onPress={() => setMissionParams({ ...missionParams, priority: level })}
            >
              <Text style={styles.priorityText}>{level}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>
    </View>
  );

  const deployWebsiteEmpire = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/website-empire/deploy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(websiteOperation)
      });
      const data = await response.json();
      Alert.alert('Success', 'Website empire deployment initiated!');
    } catch (error) {
      Alert.alert('Error', 'Failed to deploy website empire');
    } finally {
      setLoading(false);
    }
  };

  const launchNicheDomination = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/niche-domination/launch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nicheConquest)
      });
      const data = await response.json();
      Alert.alert('Success', 'Niche domination campaign launched!');
    } catch (error) {
      Alert.alert('Error', 'Failed to launch niche domination');
    } finally {
      setLoading(false);
    }
  };

  const deployAutomationArmy = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/automation/deploy-army`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(automationCommand)
      });
      const data = await response.json();
      Alert.alert('Success', 'Automation army deployed!');
    } catch (error) {
      Alert.alert('Error', 'Failed to deploy automation army');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Brotherhood Empire Command Center</Text>
      
      {renderControlPanel()}

      <ScrollView style={styles.mainContent}>
        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
            <TouchableOpacity
              style={styles.retryButton}
              onPress={fetchUpdates}
            >
              <Text style={styles.retryButtonText}>Retry Connection</Text>
            </TouchableOpacity>
          </View>
        )}

        {isLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#00ff00" />
            <Text style={styles.loadingText}>Establishing Connection...</Text>
          </View>
        )}

        <View style={styles.agentSection}>
          <Text style={styles.sectionTitle}>Deploy New Agent</Text>
          <TextInput
            style={styles.input}
            placeholder="Agent Name"
            placeholderTextColor="#666"
            value={newAgentName}
            onChangeText={setNewAgentName}
          />
          <View style={styles.agentTypes}>
            {Object.keys(AGENT_TYPES).map(type => renderAgentButton(type))}
          </View>
          {selectedAgentType && renderMissionForm()}
          <TouchableOpacity
            style={styles.deployButton}
            onPress={deployAgent}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.deployButtonText}>Deploy Agent</Text>
            )}
          </TouchableOpacity>
        </View>

        {showMissionControl && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Active Missions</Text>
            <ScrollView style={styles.missionList}>
              {Object.entries(activeMissions).map(([id, mission]: [string, any]) => (
                <View key={id} style={styles.missionItem}>
                  <Text style={styles.missionTitle}>{mission.mission?.objective || 'Unnamed Mission'}</Text>
                  <Text style={styles.missionDetail}>Status: {mission.status}</Text>
                  <Text style={styles.missionDetail}>Agents: {mission.assigned_agents?.length || 0}</Text>
                </View>
              ))}
            </ScrollView>
          </View>
        )}

        {showDigitalEmpire && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Digital Empire Control</Text>
            <TextInput
              style={styles.input}
              placeholder="Domain Name"
              value={websiteOperation.domain_name}
              onChangeText={(text) => setWebsiteOperation({...websiteOperation, domain_name: text})}
            />
            <TextInput
              style={styles.input}
              placeholder="Target Niche"
              value={websiteOperation.niche}
              onChangeText={(text) => setWebsiteOperation({...websiteOperation, niche: text})}
            />
            <TouchableOpacity
              style={styles.deployButton}
              onPress={deployWebsiteEmpire}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.deployButtonText}>Deploy Website Empire</Text>
              )}
            </TouchableOpacity>
          </View>
        )}

        {showMarketConquest && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Market Conquest Control</Text>
            <TextInput
              style={styles.input}
              placeholder="Niche Name"
              value={nicheConquest.niche_name}
              onChangeText={(text) => setNicheConquest({...nicheConquest, niche_name: text})}
            />
            <TextInput
              style={styles.input}
              placeholder="Target Locations (comma-separated)"
              value={nicheConquest.target_locations.join(', ')}
              onChangeText={(text) => setNicheConquest({
                ...nicheConquest,
                target_locations: text.split(',').map(loc => loc.trim())
              })}
            />
            <TouchableOpacity
              style={styles.deployButton}
              onPress={launchNicheDomination}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.deployButtonText}>Launch Niche Domination</Text>
              )}
            </TouchableOpacity>
          </View>
        )}

        {showAutomationForce && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Automation Force Control</Text>
            <TextInput
              style={styles.input}
              placeholder="Automation Type"
              value={automationCommand.automation_type}
              onChangeText={(text) => setAutomationCommand({...automationCommand, automation_type: text})}
            />
            <TextInput
              style={styles.input}
              placeholder="Target Processes (comma-separated)"
              value={automationCommand.target_processes.join(', ')}
              onChangeText={(text) => setAutomationCommand({
                ...automationCommand,
                target_processes: text.split(',').map(proc => proc.trim())
              })}
            />
            <TouchableOpacity
              style={styles.deployButton}
              onPress={deployAutomationArmy}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.deployButtonText}>Deploy Automation Army</Text>
              )}
            </TouchableOpacity>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Active Agents</Text>
          <ScrollView style={styles.agentList}>
            {Object.entries(activeAgents).map(([name, info]: [string, any]) => (
              <View key={name} style={styles.agentItem}>
                <Text style={styles.agentName}>{name}</Text>
                <Text style={styles.agentInfo}>Type: {info.type}</Text>
                <Text style={styles.agentInfo}>Status: {info.status}</Text>
                <Text style={styles.agentInfo}>Success Rate: {info.success_rate}%</Text>
              </View>
            ))}
          </ScrollView>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>World Domination Control</Text>
          
          <View style={styles.metricsContainer}>
            <Text style={styles.metricTitle}>Empire Value: ${(empireMetrics.empire_value / 1e12).toFixed(2)}T</Text>
            <Text style={styles.metricTitle}>Active Agents: {empireMetrics.active_agents}</Text>
            <Text style={styles.metricTitle}>Dominated Niches: {empireMetrics.dominated_niches}</Text>
          </View>

          <View style={styles.nicheSelector}>
            <Text style={styles.label}>Select Main Niche</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {Object.keys(NICHE_HIERARCHY).map((niche) => (
                <TouchableOpacity
                  key={niche}
                  style={[
                    styles.nicheButton,
                    selectedMainNiche === niche && styles.selectedNicheButton
                  ]}
                  onPress={() => setSelectedMainNiche(niche)}
                >
                  <Text style={styles.nicheButtonText}>{niche.replace('_', ' ')}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>

            {selectedMainNiche && (
              <>
                <Text style={styles.label}>Select Sub-Niche</Text>
                <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                  {Object.keys(NICHE_HIERARCHY[selectedMainNiche]).map((subNiche) => (
                    <TouchableOpacity
                      key={subNiche}
                      style={[
                        styles.nicheButton,
                        selectedSubNiche === subNiche && styles.selectedNicheButton
                      ]}
                      onPress={() => setSelectedSubNiche(subNiche)}
                    >
                      <Text style={styles.nicheButtonText}>{subNiche.replace('_', ' ')}</Text>
                    </TouchableOpacity>
                  ))}
                </ScrollView>
              </>
            )}

            <TextInput
              style={styles.input}
              placeholder="Target Location (city, state, or country)"
              value={selectedLocation}
              onChangeText={setSelectedLocation}
            />

            <Text style={styles.label}>Number of Agents: {agentCount}</Text>
            <Slider
              style={styles.slider}
              minimumValue={100}
              maximumValue={10000}
              step={100}
              value={agentCount}
              onValueChange={setAgentCount}
            />

            <Text style={styles.label}>Select API Integrations</Text>
            <ScrollView style={styles.apiContainer}>
              {Object.entries(API_INTEGRATIONS).map(([category, apis]) => (
                <View key={category} style={styles.apiCategory}>
                  <Text style={styles.apiCategoryTitle}>{category}</Text>
                  {apis.map((api) => (
                    <TouchableOpacity
                      key={api}
                      style={[
                        styles.apiButton,
                        selectedApis.includes(api) && styles.selectedApiButton
                      ]}
                      onPress={() => {
                        if (selectedApis.includes(api)) {
                          setSelectedApis(selectedApis.filter(a => a !== api));
                        } else {
                          setSelectedApis([...selectedApis, api]);
                        }
                      }}
                    >
                      <Text style={styles.apiButtonText}>{api}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              ))}
            </ScrollView>

            <TouchableOpacity
              style={styles.deployButton}
              onPress={async () => {
                try {
                  setLoading(true);
                  const response = await fetch(`${API_URL}/niche/deploy`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      main_niche: selectedMainNiche,
                      sub_niche: selectedSubNiche,
                      location: selectedLocation,
                      agent_count: agentCount,
                      api_integrations: selectedApis,
                      target_metrics: {
                        revenue_goal: 1000000,
                        market_share: 75,
                        automation_level: 95
                      },
                      automation_settings: {
                        workflow_type: "aggressive",
                        scaling_factor: "exponential",
                        operation_hours: "24/7"
                      },
                      deployment_strategy: {
                        phase_1: "market_analysis",
                        phase_2: "competitor_elimination",
                        phase_3: "rapid_scaling",
                        phase_4: "market_domination"
                      }
                    })
                  });
                  
                  const result = await response.json();
                  Alert.alert(
                    'Success',
                    `Deployed ${agentCount} agents to dominate ${selectedSubNiche} in ${selectedLocation}!`
                  );
                } catch (error) {
                  Alert.alert('Error', 'Failed to deploy niche operation');
                } finally {
                  setLoading(false);
                }
              }}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.deployButtonText}>
                  DEPLOY WORLD DOMINATION FORCE
                </Text>
              )}
            </TouchableOpacity>
          </View>
        </View>

        {/* Supreme Commander Control Panel */}
        <View style={styles.section}>
          <Text style={styles.supremeCommanderTitle}>
            Supreme Commander Control Panel - Christ Benzion
          </Text>
          
          {/* System Status */}
          <View style={styles.statusContainer}>
            <Text style={styles.statusTitle}>System Status</Text>
            <View style={styles.statusGrid}>
              <View style={styles.statusItem}>
                <Text style={styles.statusLabel}>Version</Text>
                <Text style={styles.statusValue}>{systemStatus.current_version}</Text>
              </View>
              <View style={styles.statusItem}>
                <Text style={styles.statusLabel}>Adaptation Level</Text>
                <Text style={styles.statusValue}>{systemStatus.adaptation_level}%</Text>
              </View>
              <TouchableOpacity
                style={styles.upgradeButton}
                onPress={async () => {
                  try {
                    const response = await fetch(`${API_URL}/system/upgrade`, {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' }
                    });
                    const result = await response.json();
                    Alert.alert('Success', 'System upgraded successfully');
                  } catch (error) {
                    Alert.alert('Error', 'System upgrade failed');
                  }
                }}
              >
                <Text style={styles.buttonText}>Trigger Self-Upgrade</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Agent Control */}
          <View style={styles.agentControlContainer}>
            <Text style={styles.controlTitle}>Agent Control Center</Text>
            <View style={styles.metricsGrid}>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Active Agents</Text>
                <Text style={styles.metricValue}>{agentStatus.active_agents}</Text>
              </View>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Active Missions</Text>
                <Text style={styles.metricValue}>{agentStatus.missions_in_progress}</Text>
              </View>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Loyalty Index</Text>
                <Text style={styles.metricValue}>100%</Text>
              </View>
            </View>
          </View>

          {/* Empire Analytics */}
          <View style={styles.analyticsContainer}>
            <Text style={styles.analyticsTitle}>Empire Analytics</Text>
            <View style={styles.analyticsGrid}>
              <View style={styles.analyticItem}>
                <Text style={styles.analyticLabel}>Empire Value</Text>
                <Text style={styles.analyticValue}>
                  ${(empireAnalytics.empire_value / 1e12).toFixed(2)}T
                </Text>
              </View>
              <View style={styles.analyticItem}>
                <Text style={styles.analyticLabel}>Market Dominance</Text>
                <Text style={styles.analyticValue}>
                  {Object.keys(empireAnalytics.market_dominance).length} Markets
                </Text>
              </View>
              <View style={styles.analyticItem}>
                <Text style={styles.analyticLabel}>Revenue Streams</Text>
                <Text style={styles.analyticValue}>
                  {Object.keys(empireAnalytics.revenue_streams).length} Active
                </Text>
              </View>
            </View>
          </View>

          {/* Command Interface */}
          <View style={styles.commandInterface}>
            <Text style={styles.commandTitle}>Supreme Command Interface</Text>
            <TouchableOpacity
              style={styles.commandButton}
              onPress={async () => {
                try {
                  const command = {
                    commander: "Christ Benzion",
                    type: "GLOBAL_DOMINANCE_ACCELERATION",
                    parameters: {
                      intensity: "MAXIMUM",
                      scope: "ALL_MARKETS",
                      priority: "ABSOLUTE"
                    }
                  };
                  
                  const response = await fetch(`${API_URL}/agents/command`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(command)
                  });
                  
                  const result = await response.json();
                  Alert.alert('Command Executed', 'Global dominance acceleration initiated');
                } catch (error) {
                  Alert.alert('Error', 'Command execution failed');
                }
              }}
            >
              <Text style={styles.commandButtonText}>
                ACCELERATE GLOBAL DOMINANCE
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalView}>
          <Text style={styles.modalTitle}>{modalTitle}</Text>
          <ScrollView style={styles.modalScroll}>
            {modalContent && Object.entries(modalContent).map(([key, value]) => (
              <View key={key} style={styles.modalItem}>
                <Text style={styles.modalKey}>{key}:</Text>
                <Text style={styles.modalValue}>{JSON.stringify(value, null, 2)}</Text>
              </View>
            ))}
          </ScrollView>
          <TouchableOpacity
            style={styles.closeButton}
            onPress={() => setModalVisible(false)}
          >
            <Text style={styles.closeButtonText}>Close</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  mainContent: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginVertical: 20,
  },
  controlPanel: {
    flexDirection: 'row',
    backgroundColor: '#2a2a2a',
    padding: 10,
    justifyContent: 'space-around',
  },
  controlButton: {
    padding: 10,
    borderRadius: 5,
    backgroundColor: '#3a3a3a',
  },
  activeControlButton: {
    backgroundColor: '#007AFF',
  },
  controlButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  section: {
    backgroundColor: '#2a2a2a',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
  },
  agentSection: {
    backgroundColor: '#2a2a2a',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 15,
  },
  input: {
    backgroundColor: '#3a3a3a',
    color: '#fff',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
  agentTypes: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  agentButton: {
    width: '48%',
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  selectedButton: {
    borderWidth: 2,
    borderColor: '#fff',
  },
  agentButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    textAlign: 'center',
  },
  agentDescription: {
    color: '#fff',
    fontSize: 12,
    textAlign: 'center',
    marginTop: 5,
  },
  deployButton: {
    backgroundColor: '#FF3B30',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
  },
  deployButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  missionList: {
    maxHeight: 200,
  },
  missionItem: {
    backgroundColor: '#3a3a3a',
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  missionTitle: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  missionDetail: {
    color: '#ccc',
    marginTop: 5,
  },
  agentList: {
    maxHeight: 200,
  },
  agentItem: {
    backgroundColor: '#3a3a3a',
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  agentName: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  agentInfo: {
    color: '#ccc',
    marginTop: 5,
  },
  modalView: {
    flex: 1,
    backgroundColor: '#2a2a2a',
    margin: 20,
    borderRadius: 10,
    padding: 20,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 15,
  },
  modalScroll: {
    flex: 1,
  },
  modalItem: {
    marginBottom: 10,
  },
  modalKey: {
    color: '#fff',
    fontWeight: 'bold',
  },
  modalValue: {
    color: '#ccc',
  },
  closeButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 15,
  },
  closeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  missionForm: {
    marginBottom: 15,
  },
  priorityContainer: {
    marginBottom: 15,
  },
  label: {
    color: '#fff',
    marginBottom: 5,
  },
  priorityButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  priorityButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#3a3a3a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  selectedPriority: {
    backgroundColor: '#007AFF',
  },
  priorityText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  metricsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 10,
    backgroundColor: '#1a1a1a',
    borderRadius: 10,
    marginBottom: 20
  },
  metricTitle: {
    color: '#00ff00',
    fontSize: 16,
    fontWeight: 'bold'
  },
  nicheSelector: {
    padding: 10
  },
  nicheButton: {
    backgroundColor: '#2c2c2c',
    padding: 10,
    borderRadius: 5,
    marginRight: 10,
    marginBottom: 10
  },
  selectedNicheButton: {
    backgroundColor: '#007AFF'
  },
  nicheButtonText: {
    color: '#fff',
    fontSize: 14
  },
  apiContainer: {
    maxHeight: 200
  },
  apiCategory: {
    marginBottom: 15
  },
  apiCategoryTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5
  },
  apiButton: {
    backgroundColor: '#2c2c2c',
    padding: 8,
    borderRadius: 5,
    marginRight: 10,
    marginBottom: 5
  },
  selectedApiButton: {
    backgroundColor: '#28a745'
  },
  apiButtonText: {
    color: '#fff',
    fontSize: 12
  },
  slider: {
    width: '100%',
    height: 40
  },
  deployButton: {
    backgroundColor: '#FF3B30',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 20
  },
  deployButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold'
  },
  supremeCommanderTitle: {
    color: '#FFD700',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20
  },
  statusContainer: {
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
    marginBottom: 20
  },
  statusGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap'
  },
  statusItem: {
    width: '48%',
    marginBottom: 10
  },
  statusLabel: {
    color: '#888',
    fontSize: 14
  },
  statusValue: {
    color: '#00ff00',
    fontSize: 18,
    fontWeight: 'bold'
  },
  upgradeButton: {
    backgroundColor: '#7B1FA2',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    width: '100%'
  },
  agentControlContainer: {
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
    marginBottom: 20
  },
  metricsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap'
  },
  metricItem: {
    width: '31%',
    backgroundColor: '#2c2c2c',
    padding: 10,
    borderRadius: 8,
    alignItems: 'center'
  },
  metricLabel: {
    color: '#888',
    fontSize: 12
  },
  metricValue: {
    color: '#00ff00',
    fontSize: 20,
    fontWeight: 'bold'
  },
  analyticsContainer: {
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
    marginBottom: 20
  },
  analyticsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap'
  },
  analyticItem: {
    width: '31%',
    backgroundColor: '#2c2c2c',
    padding: 10,
    borderRadius: 8,
    alignItems: 'center'
  },
  analyticLabel: {
    color: '#888',
    fontSize: 12
  },
  analyticValue: {
    color: '#00ff00',
    fontSize: 16,
    fontWeight: 'bold'
  },
  commandInterface: {
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10
  },
  commandTitle: {
    color: '#FFD700',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 15
  },
  commandButton: {
    backgroundColor: '#FF3B30',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center'
  },
  commandButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold'
  },
  errorContainer: {
    backgroundColor: '#FF3B30',
    padding: 15,
    borderRadius: 10,
    margin: 10,
    alignItems: 'center'
  },
  errorText: {
    color: '#fff',
    fontSize: 16,
    marginBottom: 10
  },
  retryButton: {
    backgroundColor: '#fff',
    padding: 10,
    borderRadius: 5
  },
  retryButtonText: {
    color: '#FF3B30',
    fontSize: 14,
    fontWeight: 'bold'
  },
  loadingContainer: {
    backgroundColor: '#1a1a1a',
    padding: 20,
    borderRadius: 10,
    margin: 10,
    alignItems: 'center'
  },
  loadingText: {
    color: '#00ff00',
    fontSize: 16,
    marginTop: 10
  }
});
